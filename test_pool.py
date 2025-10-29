import json
import logging
from tools.db_util import DbUtil
from tabulate import tabulate


def test_db_connection(config):
    """测试数据库连接是否可用 + 连接池是否复用"""
    try:
        print("🧩 开始测试数据库连接...\n")

        # 第一次创建连接
        engine1 = DbUtil.get_engine(**config)
        print(f"engine1 id: {id(engine1)}")

        # 第二次同配置创建连接（应复用）
        engine2 = DbUtil.get_engine(**config)
        print(f"engine2 id: {id(engine2)}")

        # 判断连接池是否复用
        if id(engine1) == id(engine2):
            print("✅ 同一配置连接池复用成功\n")
        else:
            print("⚠️ 不同实例创建了新的连接池，请检查 DbUtil 缓存逻辑\n")

        # 打印连接池缓存状态
        DbUtil.show_cache()

    except Exception as e:
        print(f"❌ 数据库连接测试失败：{e}")
        raise


def test_query_execution(config, sql):
    """测试 SQL 查询功能"""
    print("\n🔍 开始执行测试 SQL：", sql)

    try:
        rows = DbUtil.run_query(sql, **config)
        print("✅ 查询执行成功！返回行数：", len(rows))

        # JSON 格式输出
        print("\n📦 JSON 格式结果:")
        print(json.dumps(rows, indent=2, ensure_ascii=False))

        # Markdown 表格输出
        if rows:
            print("\n🧾 Markdown 表格结果:")
            print(tabulate(rows, headers="keys", tablefmt="github", floatfmt=""))

    except Exception as e:
        logging.exception("❌ SQL 执行异常: %s", str(e))
        print(f"❌ 查询执行失败：{e}")


if __name__ == "__main__":
    # ✅ 测试配置（根据本地数据库修改）
    config = {
        "db_type": "mysql",
        "username": "root",
        "password": "Test@666",
        "host": "127.0.0.1",
        "port": 3306,
        "database": "identity"
    }

    # 设置日志格式
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    # 测试连接池
    test_db_connection(config)

    # 测试查询
    test_query_execution(config, "SELECT 1 AS test")
