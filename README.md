# 📅 ForexFactory MCP Server

![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![MCP](https://img.shields.io/badge/MCP-Server-orange)
![uv](https://img.shields.io/badge/packaging-uv-purple)

![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-blue.svg)
![Made with Love](https://img.shields.io/badge/made%20with-%E2%9D%A4-red.svg)

An MCP (Model Context Protocol) server that exposes **ForexFactory economic calendar data** as resources and tools.

Designed for use in **agentic workflows**, LLMs, and trading assistants.


---

<details>
<summary>📂 <strong>Table of contents (click to expand)</strong></summary>
  
- [📅 ForexFactory MCP Server](#-forexfactory-mcp-server)
  - [](#)
  - [🚀 Features](#-features)
    - [📌 Development Status](#-development-status)
  - [🔧 Installation](#-installation)
    - [Requirements](#requirements)
    - [Setup](#setup)
  - [▶️ Usage](#️-usage)
    - [⚡ Quickstart](#-quickstart)
    - [SSE transport (⚠️ deprecated)](#sse-transport-️-deprecated)
    - [Environment variable defaults](#environment-variable-defaults)
  - [🏷️ Namespace](#️-namespace)
  - [📦 Resources](#-resources)
  - [🛠️ Tools](#️-tools)
  - [📝 Prompts](#-prompts)
    - [🧩 Prompt Styles](#-prompt-styles)
  - [💻 Client Examples](#-client-examples)
    - [Example: Using MCP CLI](#example-using-mcp-cli)
    - [Example: Using in Python](#example-using-in-python)
    - [Example: LangChain Integration](#example-langchain-integration)
    - [📘 Client Configuration Reference](#-client-configuration-reference)
  - [⚙️ Configuration](#️-configuration)
    - [Example `.env`](#example-env)
  - [🐳 Docker Integration](#-docker-integration)
    - [🐍 1. `uv` or dependency install fails](#-1-uv-or-dependency-install-fails)
    - [⚡ 2. Server exits immediately](#-2-server-exits-immediately)
    - [🌐 3. Port in use](#-3-port-in-use)
    - [🔐 4. Browser fails](#-4-browser-fails)
  - [🧪 Testing](#-testing)
  - [📊 Roadmap](#-roadmap)
  - [🤝 Contributing](#-contributing)
  - [📜 License](#-license)

</details>

---

## 🚀 Features

* ✅ Retrieve **economic calendar events** by time period (`today`, `this_week`, `custom`, etc.)
* ✅ Access via **MCP resources** (for subscription-style access)
* ✅ Access via **MCP tools** (direct calls from clients/agents)
* ✅ JSON-first responses for easy integration
* ⚡ Integrates with LangChain, n8n, or any MCP-compatible client

---

### 📌 Development Status

This project is **actively developed**.
The **core functionality is stable** (retrieving ForexFactory economic calendar events via MCP tools and resources), but we are still:

* Expanding features (prompts, deployment options)
* Improving documentation and examples

We welcome feedback and contributions while we continue building out the ecosystem.

---

<details>
<summary>📂 <strong>Project Structure (click to expand)</strong></summary>

```
forexfactory-mcp/
│── src/forexfactory_mcp/   # Main package
│   ├── models/             # Schemas & enums
│   ├── services/           # Scraper + data normalization
│   ├── tools/              # MCP tool definitions
│   ├── resources/          # MCP resource definitions
│   ├── prompts/            # Prompt templates (optional MCP prompts)
│   ├── utils/              # Shared helpers & config
│   └── server.py           # FastMCP server entrypoint
│
│── examples/               # Example clients
│── tests/                  # Unit tests
│── .env.example            # Copy to .env for config
│── pyproject.toml          # Dependencies & metadata
│── README.md               # Documentation
│── .python-version         # Python version pin (3.12)
```

*(See repo for full details — this is a high-level layout for contributors.)*

</details>

---

## 🔧 Installation

### Requirements

* Python 3.12+
* [uv](https://github.com/astral-sh/uv) or pip
* A modern terminal or MCP-compatible client

### Setup

```bash
# Clone repo
git clone https://github.com/kjpou1/forexfactory-mcp.git
cd forexfactory-mcp

# Install dependencies
uv sync   # or: pip install -e .

# Copy example environment and adjust if needed
cp .env.example .env
```

---

## ▶️ Usage

### ⚡ Quickstart

Start the server with default settings (`stdio` transport):

```bash
uv run ffcal-server
```

Run with HTTP transport:

```bash
uv run ffcal-server --transport http --host 0.0.0.0 --port 8080
```

---

### SSE transport (⚠️ deprecated)

```bash
uv run ffcal-server --transport sse --host 127.0.0.1 --port 8001
```

---

### Environment variable defaults

```env
MCP_TRANSPORT=http
MCP_HOST=0.0.0.0
MCP_PORT=8080
```

---

## 🏷️ Namespace

Default namespace:

```
ffcal
```

Override via `.env`:

```env
NAMESPACE=ffcal
```

---

## 📦 Resources

| Name           | Path                                 | Description          |
| -------------- | ------------------------------------ | -------------------- |
| `events_today` | `ffcal://events/today`               | Today’s events       |
| `events_week`  | `ffcal://events/week`                | All events this week |
| `events_range` | `ffcal://events/range/{start}/{end}` | Custom date range    |

---

## 🛠️ Tools

| Name                        | Type | Description                        |
| --------------------------- | ---- | ---------------------------------- |
| `ffcal_get_calendar_events` | Tool | Retrieve events for a given period |

Supported values:

```
today, tomorrow, yesterday, this_week, next_week, last_week, this_month, next_month, last_month, custom
```

---

## 📝 Prompts

| Name                        | Description                      |
| --------------------------- | -------------------------------- |
| `ffcal_daily_prep`          | Trader prep note for today       |
| `ffcal_weekly_outlook`      | Weekly macro event summary       |
| `ffcal_volatility_grid`     | Weekly event-risk heatmap        |
| `ffcal_trade_map_scenarios` | Scenario map for specific events |

---

### 🧩 Prompt Styles

All prompts support a **`style`** parameter to control formatting.
Default:

```python
style: str = "bullet points"
```

See the [Output Style Reference](docs/OUTPUT_STYLE_REFERENCE.md) for available formats.

---

## 💻 Client Examples

### Example: Using MCP CLI

```bash
mcp call ffcal:get_calendar_events time_period=this_week
```

### Example: Using in Python

```python
from mcp.client.session import Session
async with Session("ws://localhost:8000") as session:
    result = await session.call_tool("ffcal:get_calendar_events", {"time_period": "today"})
    print(result)
```

### Example: LangChain Integration

```python
from langchain.agents import initialize_agent
from langchain_mcp import MCPToolkit

toolkit = MCPToolkit.from_server_url("ws://localhost:8000", namespace="ffcal")
agent = initialize_agent(toolkit.tools)
response = agent.run("What are today’s USD-related high impact events?")
print(response)
```

---

### 📘 Client Configuration Reference

> [📖 docs/CLIENT_CONFIG_REFERENCE.md](docs/CLIENT_CONFIG_REFERENCE.md)

Includes:

* ✅ Example configs for **Claude Desktop (local + Docker)**
* 🐳 Docker build and setup
* 🧩 VS Code MCP integration (future)
* 🧪 Testing + troubleshooting checklist
* 🔍 Inspector setup for visual debugging

---

<details>
<summary>⚙️ <strong>Configuration Reference (click to expand)</strong></summary>

## ⚙️ Configuration

| Variable             | Default      | Description                             |
| -------------------- | ------------ | --------------------------------------- |
| `NAMESPACE`          | `ffcal`      | Namespace prefix                        |
| `MCP_TRANSPORT`      | `stdio`      | Transport type (`stdio`, `http`, `sse`) |
| `MCP_HOST`           | `127.0.0.1`  | Host for HTTP/SSE                       |
| `MCP_PORT`           | `8000`       | Port for HTTP/SSE                       |
| `SCRAPER_TIMEOUT_MS` | `5000`       | Playwright timeout                      |
| `LOCAL_TIMEZONE`     | System local | Timezone override                       |

---

### Example `.env`

```env
MCP_TRANSPORT=http
MCP_HOST=0.0.0.0
MCP_PORT=8080
NAMESPACE=ffcal
```

</details>

---

<details>
<summary>🐳 <strong>Docker Integration (click to expand)</strong></summary>

## 🐳 Docker Integration

Supports both **stdio** (default) and **HTTP/SSE**.

```bash
docker compose build
docker compose up forexfactory_mcp
```

Runs MCP server and exposes it on **port 8000**.

</details>

---

<details>
<summary>🧰 <strong>Makefile Targets (click to expand)</strong></summary>

| Target           | Description               |
| ---------------- | ------------------------- |
| `make build`     | Build Docker image        |
| `make run-http`  | Run server in HTTP mode   |
| `make run-stdio` | Run in stdio mode         |
| `make dev-http`  | Inspect via MCP Inspector |
| `make stop`      | Stop containers           |

</details>

---

<details>
<summary>🧩 <strong>Troubleshooting Docker (click to expand)</strong></summary>

### 🐍 1. `uv` or dependency install fails

Run:

```bash
docker compose build --no-cache forexfactory_mcp
```

### ⚡ 2. Server exits immediately

Switch to:

```bash
make run-http
```

### 🌐 3. Port in use

Change port:

```bash
docker compose run --rm -e MCP_PORT=8080 forexfactory_mcp
```

### 🔐 4. Browser fails

Install Chromium:

```bash
docker compose run forexfactory_mcp playwright install chromium
```

</details>

---

<details>
<summary>🧪 <strong>Testing & Roadmap (click to expand)</strong></summary>

## 🧪 Testing

```bash
pytest -v
```

## 📊 Roadmap

* [ ] Event filters by **currency** and **impact**
* [ ] Historical backfill
* [ ] MCP prompt expansions
* [ ] Cloud-ready deployment

</details>

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch
3. Commit with a clear message
4. Push and open a PR

---

## 📜 License

MIT License – see [LICENSE](./LICENSE) for details.

