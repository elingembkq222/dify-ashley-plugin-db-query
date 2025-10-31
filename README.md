# 🧩 ashley_plugin_db_query

**Author:** Henson  
**Version:** 0.0.1  
**Type:** Dify Tool Plugin  
**Language:** Python 3.12  

---

## 📘 简介

`ashley_plugin_db_query` 是一个 **Dify 插件 (Dify Tool)**，用于在 Dify 平台中注册 “数据库查询” 工具，支持通过 MCP（Model Context Protocol）或本地调用方式执行 SQL 查询、表结构读取、以及元数据分析。

该插件的目标是为 AI Agent / Workflow 提供 **安全、可控的数据库查询接口**，常用于数据分析、自动报表、或智能问答场景。

---

## ⚙️ 功能特性

- ✅ 支持 SQL 查询（SELECT / INSERT / UPDATE / DELETE）
- ✅ 自动连接多种数据库（MySQL / PostgreSQL / SQLite）
- ✅ 支持多租户或多数据源配置
- ✅ 查询结果结构化输出（JSON / DataFrame）
- ✅ 内置日志与错误捕获机制
- ✅ 可扩展参数验证与权限控制（例如：SQL 白名单）

---

## 📁 项目结构

```
ashley_plugin_db_query/
├── provider/
│   ├── db_query.py              # 核心逻辑：数据库查询 Provider
│
├── tools/
│   ├── sql_query.yaml           # 工具定义文件（描述 Tool 的参数与调用方式）
│
├── main.py                      # 插件入口（注册 Provider / 启动服务）
├── requirements.txt             # 依赖包
├── README.md                    # 插件说明文件（即本文件）
└── venv312/                     # 本地虚拟环境 (可选)
```

---

## 🚀 本地开发与测试

### 1️⃣ 启动虚拟环境
```bash
source venv312/bin/activate
```

### 2️⃣ 启动插件
```bash
python main.py
```

> 启动后会在控制台打印日志，确认注册成功后即可在 Dify 开发模式中使用。

---

## 🧩 构建 Dify 插件包

执行以下命令可生成 `.difypkg` 插件包：

```bash
dify plugin package . -o test.difypkg
```

生成成功后，会在项目根目录下输出：

```
test.difypkg
```

可直接在 Dify 后台「插件管理 → 导入插件」中上传使用。

---

## 🧱 示例工具定义（`tools/sql_query.yaml`）

```yaml
identity:
  name: db_query
  author: henson
  label:
    zh_Hans: 数据库查询
    en_US: Database Query
  description:
    zh_Hans: 用于执行 SQL 相关工具。
    en_US: Database Query Provider for executing SQL-related tools.
  icon: _assets/icon.svg

extra:
  python:
    source: provider/db_query.py

tools:
  - path: tools/sql_query.yaml
```

---

## 🔧 Provider 示例（`provider/db_query.py`）

```python
import sqlite3
from dify_plugin.core.provider import ToolProvider

class DatabaseQueryProvider(ToolProvider):
    def execute(self, query: str):
        try:
            conn = sqlite3.connect("example.db")
            cur = conn.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            conn.close()
            return {"success": True, "rows": rows}
        except Exception as e:
            return {"success": False, "error": str(e)}
```

---

## 🧾 Git 版本管理

### 标记发布版本
```bash
git tag -a v1.0.0 -m "发布版本 1.0.0"
git push origin v1.0.0
```

> 建议每次发布前更新版本号，并同步推送标签。

---

## 🧰 常见问题

| 问题 | 解决方案 |
|------|------------|
| 启动时报错 `ModuleNotFoundError` | 检查虚拟环境依赖是否安装：`pip install -r requirements.txt` |
| 打包时提示 `tool_provider.yaml not found` | 确保 `sql_query.yaml` 位于 `tools/` 目录 |
| 插件导入后未显示工具 | 检查 `main.py` 中是否正确注册 Provider |

---

## 🧑‍💻 开发者信息

| 字段 | 值 |
|------|----|
| Author | Henson Cheng |
| Email | （可选填写） |
| Repo | private / GitHub / internal |
| License | MIT |

---

## 🧭 未来计划

- 支持多数据库连接配置（通过环境变量或 YAML）
- 增强 SQL 安全审查（防止危险操作）
- 增加分页与表结构元数据工具
- 与 Dify Workflows 深度集成，实现 Agent 数据问答

---

## 🪪 License

This project is licensed under the **MIT License**.  
Copyright © 2025 Henson.
