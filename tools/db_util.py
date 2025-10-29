import datetime
import logging
import threading
from typing import Optional
from urllib import parse
from uuid import UUID
from sqlalchemy import create_engine, text

try:
    import oracledb
except ImportError:
    oracledb = None
    logging.warning("⚠️ 未检测到 oracledb 模块，如需连接 Oracle，请先执行 `pip install oracledb`")


class DbUtil:
    _engine_cache = {}
    _lock = threading.Lock()

    @classmethod
    def _make_key(cls, db_type, username, host, port, database):
        return f"{db_type}:{username}@{host}:{str(port)}:{database or ''}"

    @classmethod
    def _get_driver_name(cls, db_type):
        db_type = db_type.lower()
        if db_type == 'mysql':
            return 'mysql+pymysql'
        elif db_type in {'oracle', 'oracle11g'}:
            return 'oracle+oracledb'
        elif db_type == 'postgresql':
            return 'postgresql+psycopg2'
        elif db_type == 'mssql':
            return 'mssql+pymssql'
        else:
            raise ValueError(f"不支持的数据库类型: {db_type}")

    @classmethod
    def _create_engine(cls, db_type, username, password, host, port, database, properties=None):
        driver = cls._get_driver_name(db_type)
        parsed_username = parse.quote_plus(username)
        parsed_password = parse.quote_plus(password)
        parsed_host = parse.quote_plus(host)
        url = f"{driver}://{parsed_username}:{parsed_password}@{parsed_host}"
        if port:
            url += f":{port}"
        url += "/"
        if database:
            url += parse.quote_plus(database)
        if properties:
            url += f"?{properties}"
        if db_type == 'oracle11g' and oracledb:
            try:
                oracledb.init_oracle_client()
            except Exception as e:
                logging.warning(f"初始化 Oracle 客户端失败：{e}")
        logging.info(f"🧩 创建数据库引擎: {url}")
        return create_engine(url, pool_size=10, pool_recycle=1800)

    @classmethod
    def get_engine(cls, db_type: str,
                   username: str, password: str,
                   host: str, port: Optional[str] = None,
                   database: Optional[str] = None,
                   properties: Optional[str] = None):
        key = cls._make_key(db_type, username, host, port, database)
        if key not in cls._engine_cache:
            with cls._lock:
                if key not in cls._engine_cache:
                    engine = cls._create_engine(db_type, username, password, host, port, database, properties)
                    cls._engine_cache[key] = engine
                    print(f"🆕 创建新连接池: {key}")
        else:
            print(f"♻️ 复用连接池: {key}")
        return cls._engine_cache[key]

    @classmethod
    def run_query(cls, query_sql: str, **config) -> list[dict]:
        engine = cls.get_engine(**config)
        query_sql = query_sql.replace('%', '%%')
        with engine.connect() as conn:
            result = conn.execute(text(query_sql))
            rows = [dict(row._mapping) for row in result]
        for record in rows:
            for key, val in record.items():
                if isinstance(val, datetime.datetime):
                    record[key] = val.strftime('%Y-%m-%d %H:%M:%S')
                elif isinstance(val, datetime.date):
                    record[key] = val.strftime('%Y-%m-%d')
                elif isinstance(val, UUID):
                    record[key] = str(val)
        return rows

    @classmethod
    def show_cache(cls):
        print("🔍 当前连接池缓存:")
        for key, engine in cls._engine_cache.items():
            print(f"  - {key} → id={id(engine)}")
