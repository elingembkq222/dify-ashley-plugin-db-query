from dify_plugin import ToolProvider
from tools.db_util import DbUtil

class DbQueryProvider(ToolProvider):
    """数据库 Provider：校验连接配置 + 提供 Engine 复用"""

    def _validate_credentials(self, credentials: dict) -> None:
        db_type = credentials.get("db_type")
        host = credentials.get("db_host")
        port = credentials.get("db_port") or 3306
        username = credentials.get("db_username")
        password = credentials.get("db_password")
        database = credentials.get("db_name", "")

        # 测试连接
        engine = DbUtil.get_engine(
            db_type=db_type,
            username=username,
            password=password,
            host=host,
            port=port,
            database=database
        )
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return
