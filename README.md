# 📅 ForexFactory MCP Server

> An MCP (Model Context Protocol) server that exposes **ForexFactory economic calendar data** as resources and tools.  
> Designed for use in **agentic workflows**, LLMs, and trading assistants.

---

## 🚀 Features

- ✅ Retrieve **economic calendar events** by time period (`today`, `this_week`, `custom`, etc.)
- ✅ Access via **MCP resources** (for subscription-style access)
- ✅ Access via **MCP tools** (direct calls from clients/agents)
- ✅ JSON-first responses for easy integration
- ⚡ Integrates with LangChain, n8n, or any MCP-compatible client

---

### 📂 Project Structure

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


---

## 🔧 Installation

### Requirements
- Python 3.12+  (see `.python-version` for exact version)
- [uv](https://github.com/astral-sh/uv) or pip
- A modern terminal or MCP-compatible client

### Setup

```bash
# Clone repo
git clone https://github.com/yourusername/forexfactory-mcp.git
cd forexfactory-mcp

# Install dependencies
uv sync   # or: pip install -e .

# Copy example environment and adjust if needed
cp .env.example .env
````

---

## ▶️ Usage

### Start the MCP server

```bash
uv run forexfactory_mcp.server
```

The server will expose MCP **resources** and **tools** that clients can call.

---

## 🏷️ Namespace

This MCP server registers under the namespace:

```
ffcal
```

You can override this in your `.env` file:

```env
NAMESPACE=ffcal
```

All tools and resources are exposed with this prefix.

Examples:

* `ffcal:get_calendar_events`
* `ffcal:events_week`
* `ffcal:events_today`

---

## 🛠️ Tools & Resources

| Name                  | Type     | Description                        | Parameters                                                              |
| --------------------- | -------- | ---------------------------------- | ----------------------------------------------------------------------- |
| `events_today`        | Resource | Fetch today’s calendar events      | None                                                                    |
| `events_week`         | Resource | Fetch this week’s events           | None                                                                    |
| `get_calendar_events` | Tool     | Retrieve events for a given period | `time_period` (str), `start_date` (YYYY-MM-DD), `end_date` (YYYY-MM-DD) |

### Supported `time_period` values

```
today, tomorrow, yesterday,
this_week, next_week, last_week,
this_month, next_month, last_month,
custom
```

When `custom` is used, you must pass `start_date` and `end_date`.

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

## ⚙️ Configuration

No special config is required, but you may set environment variables:

| Variable      | Default                                 | Description                               |
| ------------- | --------------------------------------- | ----------------------------------------- |
| `NAMESPACE`   | `ffcal`                                 | MCP namespace for tools/resources         |
| `FF_BASE_URL` | `https://www.forexfactory.com/calendar` | Base URL for scraping                     |
| `CACHE_TTL`   | `300`                                   | Cache time (seconds) for repeated queries |

### Example `.env`

Copy `.env.example` to `.env` and adjust values as needed:

```bash
cp .env.example .env
```

Example content:

```env
# Namespace for MCP resources/tools
NAMESPACE=ffcal

# Base URL for ForexFactory scraping
FF_BASE_URL=https://www.forexfactory.com/calendar

# Cache time in seconds (default: 300)
CACHE_TTL=300

# Timeout for Playwright in milliseconds
SCRAPER_TIMEOUT_MS=5000

# Local timezone override (uses system local if not set)
#LOCAL_TIMEZONE=Europe/Luxembourg

# Control which fields to include/exclude in normalized event data
# INCLUDE_FIELDS supports wildcards (*)
INCLUDE_FIELDS=
EXCLUDE_FIELDS=
```

---

## 🧪 Testing

```bash
pytest -v
```

---

## 📊 Roadmap

* [ ] Event filters by **currency** and **impact**
* [ ] Historical event backfill
* [ ] In-memory caching (to reduce repeated scraping)
* [ ] Docker container for deployment
* [ ] MCP prompts for querying events in natural language

---

## 🤝 Contributing

1. Fork this repo
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit changes: `git commit -m "Add my feature"`
4. Push branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📜 License

MIT License – see [LICENSE](./LICENSE) for details.

