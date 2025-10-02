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

No special config is required, but you may set environment variables.

| Variable             | Default                                 | Description                                                                 |
| -------------------- | --------------------------------------- | --------------------------------------------------------------------------- |
| `NAMESPACE`          | `ffcal`                                 | MCP namespace for tools/resources                                           |
| `FF_BASE_URL`        | `https://www.forexfactory.com/calendar` | Base URL for scraping ForexFactory calendar data                            |
| `CACHE_TTL`          | `300`                                   | Cache time (seconds) for repeated queries                                   |
| `SCRAPER_TIMEOUT_MS` | `5000`                                  | Timeout for Playwright (milliseconds)                                       |
| `LOCAL_TIMEZONE`     | system local (fallback UTC)             | Local timezone override (e.g., `Europe/Luxembourg`)                         |
| `INCLUDE_FIELDS`     | *(empty → all fields)*                  | Comma-separated list of fields to include (supports wildcards `*`)          |
| `EXCLUDE_FIELDS`     | *(empty → none)*                        | Comma-separated list of fields to exclude (ignored if `INCLUDE_FIELDS` set) |

---

### Include/Exclude Fields

You can control which event fields are returned by the MCP server using
`INCLUDE_FIELDS` and `EXCLUDE_FIELDS`.

#### Processing Rules

1. If **both are empty** → the server returns a **default lean set**:

```

id, title, currency, impact, datetime, forecast, previous, actual

````

2. If **`INCLUDE_FIELDS=*`** → all available fields are included.

3. If **`INCLUDE_FIELDS` is set** → only the specified fields are included.  
- Example:
  ```env
  INCLUDE_FIELDS=id,name,currency,date,forecast,previous,actual
  ```

4. If **both `INCLUDE_FIELDS` and `EXCLUDE_FIELDS` are set** →  
- First, apply `INCLUDE_FIELDS`.  
- Then, remove any fields listed in `EXCLUDE_FIELDS`.  

#### Example Configurations

```env
# Default lean set (no INCLUDE/EXCLUDE set)
INCLUDE_FIELDS=
EXCLUDE_FIELDS=

# All fields
INCLUDE_FIELDS=*
EXCLUDE_FIELDS=

# Minimal fields
INCLUDE_FIELDS=id,name,currency,date,forecast,previous,actual

# Include impact fields, but exclude noisy metadata
INCLUDE_FIELDS=impact*,date,currency
EXCLUDE_FIELDS=dateline,hasLinkedThreads
````

---

### Supported Fields

| Category         | Fields                                                                                                                                                               |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Identity**     | `id`, `ebaseId`, `title`, `name`, `prefixedName`, `trimmedPrefixedName`                                                                                              |
| **Titles**       | `soloTitle`, `soloTitleFull`, `soloTitleShort`                                                                                                                       |
| **Metadata**     | `notice`, `dateline`, `country`, `currency`                                                                                                                          |
| **Links**        | `url`, `soloUrl`, `editUrl`, `hasLinkedThreads`, `siteId`                                                                                                            |
| **Status Flags** | `hasNotice`, `hasDataValues`, `hasGraph`, `checkedIn`, `isMasterList`, `firstInDay`, `greyed`, `upNext`                                                              |
| **Impact**       | `impact`, `impactName`, `impactClass`, `impactTitle`                                                                                                                 |
| **Timing**       | `datetime`, `timeLabel`, `timeMasked`, `date`                                                                                                                        |
| **Values**       | `actual`, `previous`, `revision`, `forecast`, `leaked`, `actualBetterWorse`, `revisionBetterWorse`                                                                   |
| **Display**      | `showGridLine`, `hideHistory`, `hideSoloPage`, `showDetails`, `showGraph`, `enableDetailComponent`, `enableExpandComponent`, `enableActualComponent`, `showExpanded` |

```


---

### Example `.env`

```env
# =====================================================
# 🌐 MCP Namespace
# =====================================================
# Namespace prefix for all tools and resources.
# Default: ffcal
NAMESPACE=ffcal


# =====================================================
# ⚙️ Scraper Configuration
# =====================================================
# Timeout for Playwright in milliseconds
# Default: 5000 (5s)
SCRAPER_TIMEOUT_MS=2000

# Local timezone override (uses system local if not set)
# Example: Europe/Luxembourg
#LOCAL_TIMEZONE=Europe/Luxembourg


# =====================================================
# 📊 Event Fields
# =====================================================
# Control which fields to include/exclude in normalized event data.
# - If both are empty, all fields are included.
# - If both are set, INCLUDE_FIELDS takes precedence.
# - INCLUDE_FIELDS supports wildcard (*) to include all fields.
#   Example: INCLUDE_FIELDS=*
#     → includes all fields

INCLUDE_FIELDS=
EXCLUDE_FIELDS=

# Example usage:
# INCLUDE_FIELDS=id,name,country,currency,date,actual,forecast,previous
# EXCLUDE_FIELDS=notice,dateline,hasLinkedThreads,checkedIn,firstInDay

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

