from tools.db_util import DbUtil

if __name__ == "__main__":
    config = {
        "db_type": "mysql",
        "username": "root",
        "password": "Test@666",
        "host": "127.0.0.1",
        "port": 3306,
        "database": "identity"
    }

    engine1 = DbUtil.get_engine(**config)
    engine2 = DbUtil.get_engine(**config)
    print("engine1 id:", id(engine1))
    print("engine2 id:", id(engine2))

    if id(engine1) == id(engine2):
        print("✅ 同一配置连接池复用成功")
    else:
        print("⚠️ 不同实例创建了新的连接池")

    DbUtil.show_cache()

    rows = DbUtil.run_query("SELECT 1 as test", **config)
    print(rows)
