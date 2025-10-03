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

* Python 3.12+  (see `.python-version` for exact version)
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

### Start the MCP server

```bash
uv run forexfactory_mcp.server
```

The server will expose MCP **resources**, **prompts**, and **tools** that clients can call.

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

* `ffcal_get_calendar_events`
* `ffcal:events_week`
* `ffcal:events_today`

---

## 📦 Resources

Resources expose **economic calendar events** for fixed time windows or a custom date range.
They are useful for **streaming or subscription-based access** to calendar data.

| Name                | Path                                 | Description                                  |
| ------------------- | ------------------------------------ | -------------------------------------------- |
| `events_today`      | `ffcal://events/today`               | Economic calendar events scheduled for today |
| `events_yesterday`  | `ffcal://events/yesterday`           | Events from yesterday                        |
| `events_tomorrow`   | `ffcal://events/tomorrow`            | Events scheduled for tomorrow                |
| `events_week`       | `ffcal://events/week`                | All events this week                         |
| `events_this_week`  | `ffcal://events/this_week`           | Explicit alias for this week’s events        |
| `events_next_week`  | `ffcal://events/next_week`           | All events scheduled for next week           |
| `events_last_week`  | `ffcal://events/last_week`           | Events from last week                        |
| `events_this_month` | `ffcal://events/this_month`          | All events scheduled for this month          |
| `events_next_month` | `ffcal://events/next_month`          | All events scheduled for next month          |
| `events_last_month` | `ffcal://events/last_month`          | Events from last month                       |
| `events_range`      | `ffcal://events/range/{start}/{end}` | Custom date range (YYYY-MM-DD to YYYY-MM-DD) |

---

## 🛠️ Tools

Tools are **direct, parameterized calls** that allow you to query economic events dynamically.

| Name                        | Type | Description                        | Parameters                                                              |
| --------------------------- | ---- | ---------------------------------- | ----------------------------------------------------------------------- |
| `ffcal_get_calendar_events` | Tool | Retrieve events for a given period | `time_period` (str), `start_date` (YYYY-MM-DD), `end_date` (YYYY-MM-DD) |

### Supported `time_period` values

```
today, tomorrow, yesterday,
this_week, next_week, last_week,
this_month, next_month, last_month,
custom
```

When `custom` is used, you must also pass `start_date` and `end_date`.

---

## 📝 Prompts

Unlike **resources** (which return structured event data) and **tools** (which query events dynamically),
**prompts generate structured text outputs** — trader notes, playbooks, and scenario analyses — that can be directly integrated into workflows or reports.

All prompt names are prefixed with the configured **namespace** (default: `ffcal_`).
If you override `NAMESPACE` in your `.env`, replace the prefix accordingly.

| Name                             | Description                                                    | Why Use                                                                        |
| -------------------------------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `ffcal_daily_prep`               | Summarize today’s calendar into a **trader prep note**.        | Quick morning scan to know which events matter today.                          |
| `ffcal_daily_playbook`           | Generate an **FX daily trading playbook** for today.           | Structured trade plan aligned with key macro drivers.                          |
| `ffcal_weekly_outlook`           | Summarize **upcoming week’s high-impact events**.              | Helps prepare positioning for the week ahead.                                  |
| `ffcal_weekly_outlook_next_week` | Draft a **Sunday note** for next week’s events.                | Pre-market research note for weekend review.                                   |
| `ffcal_cross_asset_radar`        | Cross-asset spillover **radar** relevant to FX markets.        | Highlights risks from equities, bonds, and commodities that may spill into FX. |
| `ffcal_positioning_flow_note`    | Note on **positioning, ETF flows, and options expiries**.      | Capture sentiment and positioning context beyond the economic calendar.        |
| `ffcal_volatility_grid`          | **Weekly event-risk heatmap** presented as a grid.             | Visualize which days/times carry the most volatility risk.                     |
| `ffcal_trade_map_scenarios`      | Scenario map for a **chosen event** with trading implications. | Anticipate market reactions and map trade scenarios ahead of the release.      |

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

| Variable             | Default                     | Description                                                              |
| -------------------- | --------------------------- | ------------------------------------------------------------------------ |
| `NAMESPACE`          | `ffcal`                     | MCP namespace for tools/resources                                        |
| `MCP_TRANSPORT`      | `stdio`                     | Transport type: `stdio`, `http`, or `sse`                                |
| `MCP_HOST`           | `127.0.0.1`                 | Host for HTTP/SSE transport (ignored for stdio)                          |
| `MCP_PORT`           | `8000`                      | Port for HTTP/SSE transport (ignored for stdio)                          |
| `SCRAPER_TIMEOUT_MS` | `5000`                      | Timeout for Playwright (milliseconds)                                    |
| `LOCAL_TIMEZONE`     | system local (fallback UTC) | Local timezone override (e.g., `Europe/Luxembourg`)                      |
| `INCLUDE_FIELDS`     | *(empty → default fields)*  | Comma-separated list of fields to include, or `*` for all fields         |
| `EXCLUDE_FIELDS`     | *(empty → none)*            | Comma-separated list of fields to exclude (applied after INCLUDE_FIELDS) |

---

### Include/Exclude Fields

You can control which event fields are returned by the MCP server using
`INCLUDE_FIELDS` and `EXCLUDE_FIELDS`.

#### Processing Rules

1. If **both are empty** → the server returns a **default lean set**:

   ```
   id, title, currency, impact, datetime, forecast, previous, actual
   ```

2. If **`INCLUDE_FIELDS=*`** → all available fields are included.

3. If **`INCLUDE_FIELDS` is set** → only the specified fields are included.
   Example:

   ```env
   INCLUDE_FIELDS=id,name,currency,date,forecast,previous,actual
   ```

4. If **both `INCLUDE_FIELDS` and `EXCLUDE_FIELDS` are set** →

   * First, apply `INCLUDE_FIELDS`.
   * Then, remove any fields listed in `EXCLUDE_FIELDS`.

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
INCLUDE_FIELDS=impactName,impactClass,date,currency
EXCLUDE_FIELDS=dateline,hasLinkedThreads
```

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
# 🚦 MCP Server Transport
# =====================================================
# Transport type for MCP server
# Options: stdio | http | sse
# Default: stdio
MCP_TRANSPORT=stdio

# Host for HTTP/SSE transport (ignored for stdio)
# Default: 127.0.0.1
MCP_HOST=127.0.0.1

# Port for HTTP/SSE transport (ignored for stdio)
# Default: 8000
MCP_PORT=8000

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
# - If both are empty, only the default lean set of fields is included.
# - If INCLUDE_FIELDS=* → all fields are included.
# - If both are set, INCLUDE_FIELDS is applied first, then EXCLUDE_FIELDS removes fields.

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
