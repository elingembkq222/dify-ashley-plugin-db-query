import logging
from typing import Any
from collections.abc import Generator

import sqlparse
import tabulate
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from tools.db_util import DbUtil


class SqlQueryTool(Tool):
    """执行 SQL 查询的 Dify 插件工具"""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """核心执行逻辑"""
        # ✅ 参数解析 + 校验
        db_type = tool_parameters.get("db_type", "").strip().lower()
        if not db_type:
            raise ValueError("Please select the database type")

        db_host = tool_parameters.get("db_host", "").strip()
        if not db_host:
            raise ValueError("Please fill in the database host")

        db_port = tool_parameters.get("db_port")
        if db_port is not None:
            db_port = str(db_port)

        db_username = tool_parameters.get("db_username", "").strip()
        if not db_username:
            raise ValueError("Please fill in the database username")

        db_password = tool_parameters.get("db_password", "")
        if not db_password:
            raise ValueError("Please fill in the database password")

        db_name = tool_parameters.get("db_name", "").strip()
        db_properties = tool_parameters.get("db_properties", "").strip()

        query_sql = tool_parameters.get("query_sql", "").strip()
        if not query_sql:
            raise ValueError("Please fill in the query SQL, for example: select * from tbl_name")

        # ✅ 只允许执行 SELECT 查询，防止危险 SQL
        statements = sqlparse.parse(query_sql)
        if len(statements) != 1:
            raise ValueError("Only a single SQL statement is allowed")
        if statements[0].get_type() != "SELECT":
            raise ValueError("Only SELECT statements are allowed")

        output_format = tool_parameters.get("output_format", "json").lower()

        # ✅ 提前通知前端「正在执行」
        yield self.create_text_message("⏳ Executing SQL query...")

        try:
            # ✅ 使用连接池（自动复用）
            rows = DbUtil.run_query(
                query_sql=query_sql,
                db_type=db_type,
                username=db_username,
                password=db_password,
                host=db_host,
                port=db_port,
                database=db_name,
                properties=db_properties,
            )

            logging.info(f"✅ Query completed, rows={len(rows)}")

            # ✅ 没有结果
            if not rows:
                yield self.create_text_message("✅ Query executed successfully, but no data returned.")
                return

            # ✅ 分步返回：行数提示
            yield self.create_text_message(f"✅ Query succeeded, {len(rows)} rows retrieved.")

            # ✅ 格式化输出
            if output_format == "json":
                yield self.create_json_message(rows)
            else:
                text = tabulate.tabulate(rows, headers="keys", tablefmt="github", floatfmt="")
                yield self.create_text_message(text)

        except Exception as e:
            logging.exception("❌ SQL query execution failed: %s", str(e))
            yield self.create_text_message(f"❌ Query failed: {str(e)}")
