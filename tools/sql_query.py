from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from typing import Any
from collections.abc import Generator
from tools.db_util import DbUtil

class SqlQueryTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        credentials = self.runtime.credentials
        provider = self.runtime.provider
        query_sql = tool_parameters.get("query_sql")
        output_format = tool_parameters.get("output_format", "json")

        try:
            rows = DbUtil.run_query(query_sql, **credentials)
            if not rows:
                yield self.create_text_message("✅ 查询成功，无结果返回。")
            elif output_format == "json":
                yield self.create_json_message(rows)
            else:
                yield self.create_text_message(self._to_markdown(rows))
        except Exception as e:
            yield self.create_text_message(f"❌ 查询失败: {str(e)}")

    def _to_markdown(self, rows):
        if not rows:
            return "（无数据）"
        headers = rows[0].keys()
        lines = ["| " + " | ".join(headers) + " |"]
        lines.append("|" + "|".join(["---"] * len(headers)) + "|")
        for row in rows:
            lines.append("| " + " | ".join(str(row[h]) for h in headers) + " |")
        return "\n".join(lines)
