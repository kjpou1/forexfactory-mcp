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

- [📅 ForexFactory MCP Server](#-forexfactory-mcp-server)
  - [🚀 Features](#-features)
    - [📌 Development Status](#-development-status)
    - [📂 Project Structure](#-project-structure)
  - [🔧 Installation](#-installation)
    - [Requirements](#requirements)
    - [Setup](#setup)
  - [▶️ Usage](#️-usage)
    - [⚡ Quickstart](#-quickstart)
    - [Start the MCP server (default: stdio)](#start-the-mcp-server-default-stdio)
    - [Change transport to HTTP](#change-transport-to-http)
    - [SSE transport (⚠️ deprecated, use HTTP if possible)](#sse-transport-️-deprecated-use-http-if-possible)
    - [Environment variable defaults](#environment-variable-defaults)
    - [Summary of precedence](#summary-of-precedence)
  - [🏷️ Namespace](#️-namespace)
  - [📦 Resources](#-resources)
  - [🛠️ Tools](#️-tools)
    - [Supported `time_period` values](#supported-time_period-values)
  - [📝 Prompts](#-prompts)
    - [🧩 Prompt Styles](#-prompt-styles)
      - [💡 Example – Default Behavior](#-example--default-behavior)
      - [🎨 Example – Custom Style](#-example--custom-style)
      - [🧠 Developer Note](#-developer-note)
  - [💻 Client Examples](#-client-examples)
    - [Example: Using MCP CLI](#example-using-mcp-cli)
    - [Example: Using in Python](#example-using-in-python)
    - [Example: LangChain Integration](#example-langchain-integration)
    - [📘 Client Configuration Reference](#-client-configuration-reference)
  - [⚙️ Configuration](#️-configuration)
    - [Include/Exclude Fields](#includeexclude-fields)
      - [Processing Rules](#processing-rules)
      - [Example Configurations](#example-configurations)
    - [Supported Fields](#supported-fields)
    - [Example `.env`](#example-env)
  - [🐳 Docker Integration](#-docker-integration)
    - [🧱 Build the image](#-build-the-image)
    - [▶️ Run (default: stdio)](#️-run-default-stdio)
    - [🌐 Run in HTTP mode](#-run-in-http-mode)
    - [🧾 Using a `.env` file](#-using-a-env-file)
  - [🧰 Makefile Targets](#-makefile-targets)
    - [Example usage](#example-usage)
    - [🧩 Inspector / Debugging](#-inspector--debugging)
    - [🧹 Cleanup](#-cleanup)
    - [📦 Docker Compose Overview](#-docker-compose-overview)
    - [✅ Summary](#-summary)
  - [🧩 Troubleshooting Docker](#-troubleshooting-docker)
    - [🐍 1. `uv` or dependency install fails during build](#-1-uv-or-dependency-install-fails-during-build)
    - [⚡ 2. Server starts but shuts down immediately](#-2-server-starts-but-shuts-down-immediately)
    - [🌐 3. Port already in use (`[Errno 98] Address already in use`)](#-3-port-already-in-use-errno-98-address-already-in-use)
    - [🔐 4. Playwright browser fails to start](#-4-playwright-browser-fails-to-start)
    - [🧱 5. `mcp dev` fails with “No server object found”](#-5-mcp-dev-fails-with-no-server-object-found)
    - [📦 6. `.env` changes not taking effect](#-6-env-changes-not-taking-effect)
    - [🧰 7. Viewing container logs](#-7-viewing-container-logs)
    - [🧼 8. Cleaning up everything](#-8-cleaning-up-everything)
    - [✅ Quick Checklist](#-quick-checklist)
  - [🧪 Testing](#-testing)
  - [📊 Roadmap](#-roadmap)
  - [🤝 Contributing](#-contributing)
  - [📜 License](#-license)


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

### ⚡ Quickstart

Start the server with default settings (`stdio` transport):

```bash
uv run ffcal-server
```

Or directly with Python:

```bash
python -m forexfactory_mcp.server
```

Run with HTTP transport on port 8080:

```bash
uv run ffcal-server --transport http --host 0.0.0.0 --port 8080
```

---

### Start the MCP server (default: stdio)

```bash
uv run ffcal-server
```

or directly with Python:

```bash
python -m forexfactory_mcp.server
```

---

### Change transport to HTTP

```bash
uv run ffcal-server --transport http --host 0.0.0.0 --port 8080
```

or:

```bash
python -m forexfactory_mcp.server --transport http --host 0.0.0.0 --port 8080
```

This runs the server on **[http://0.0.0.0:8080/mcp](http://0.0.0.0:8080/mcp)** (streamable HTTP transport).

---

### SSE transport (⚠️ deprecated, use HTTP if possible)

```bash
uv run ffcal-server --transport sse --host 127.0.0.1 --port 8001
```

---

### Environment variable defaults

Instead of passing CLI flags every time, you can set them in `.env`:

```env
MCP_TRANSPORT=http
MCP_HOST=0.0.0.0
MCP_PORT=8080
```

Then simply run:

```bash
uv run ffcal-server
```

---

### Summary of precedence

1. CLI flags (`--transport`, `--host`, `--port`)
2. `.env` settings (`MCP_TRANSPORT`, `MCP_HOST`, `MCP_PORT`)
3. Hardcoded defaults (`stdio`, `127.0.0.1`, `8000`)

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

### 🧩 Prompt Styles

All prompts support a **`style`** parameter that controls *how* the model formats and presents its output.  
This acts as a **presentation layer selector**, letting you choose between clean reports, emoji-rich summaries, or persona-driven tones — without changing the underlying logic of the prompt.

```python
style: str = "bullet points"
````

If no style is specified, prompts default to `bullet points`, ensuring simple and readable output suitable for terminals, dashboards, or note integrations.

#### 💡 Example – Default Behavior

**Prompt Call**

```python
ffcal_weekly_outlook(style="bullet points")
```

**Output**

```
• USD: ADP and ISM data highlight employment softening.
• EUR: CPI steady near target; limited policy urgency.
• JPY: BOJ comments drive mild volatility in Asia.
• AUD: RBA hold and China PMI rebound lift risk tone.
```

#### 🎨 Example – Custom Style

You can switch the visual tone dynamically using any supported style from the catalog
(see [docs/OUTPUT_STYLE_REFERENCE.md](docs/OUTPUT_STYLE_REFERENCE.md)).

**Prompt Call**

```python
ffcal_weekly_outlook(style="colored devil faces 😈")
```

**Output**

```
😈🔥 USD weakens after ISM miss — risk-on mood.
😈🟩 EUR steady after CPI; positioning flat.
😈🟥 JPY squeezes shorts post-Ueda speech.
```

#### 🧠 Developer Note

| Parameter | Type  | Default           | Description                                                                                                                    |
| --------- | ----- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `style`   | `str` | `"bullet points"` | Defines the output’s formatting and tone. Accepts any style from the [Output Style Reference](docs/OUTPUT_STYLE_REFERENCE.md). |

This style system keeps prompts **modular and presentation-agnostic**.
The underlying logic remains the same — only the *rendering layer* changes.
This makes it easy to reuse a single prompt definition across dashboards, LLM clients, or chat workflows while maintaining a consistent visual identity.

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

### 📘 Client Configuration Reference

For detailed setup instructions on connecting **Claude Desktop**, **VS Code**, or the **MCP Inspector** to the ForexFactory MCP Server,
see the full guide:

> [📖 docs/CLIENT_CONFIG_REFERENCE.md](docs/CLIENT_CONFIG_REFERENCE.md)

This includes:

* ✅ Example configs for **Claude Desktop (local + Docker)**
* 🐳 Build instructions for Docker-based MCP servers
* 🧩 Future support notes for **VS Code MCP extension**
* 🧪 Testing + troubleshooting checklist
* 🔍 Inspector setup for visual debugging


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

## 🐳 Docker Integration

The **ForexFactory MCP Server** ships with a fully configured **Dockerfile** and **docker-compose.yml** for easy deployment and cross-environment reproducibility.
It supports both **stdio** (default) and **HTTP/SSE** transport modes.

---

### 🧱 Build the image

```bash
docker compose build
```

This uses the project’s `Dockerfile` to:

* Install dependencies via **uv**
* Set up Playwright (for headless scraping)
* Expose port **8000** for HTTP mode
* Bundle the MCP server ready for `stdio` or `http` transport

---

### ▶️ Run (default: stdio)

```bash
docker compose up forexfactory_mcp
```

The server runs in **stdio** mode by default and waits for MCP client connections.

Logs will stream directly to your terminal:

```
[10/04/25 09:27:16] INFO  ✅ ForexFactory MCP server initialized, waiting for client…
```

---

### 🌐 Run in HTTP mode

Use environment variables to override the defaults:

```bash
docker compose run --rm --service-ports \
  -e MCP_TRANSPORT=http \
  -e MCP_HOST=0.0.0.0 \
  -e MCP_PORT=8000 \
  forexfactory_mcp
```

This starts the MCP server over HTTP and makes it available at:

> **[http://localhost:8000/.well-known/mcp/manifest.json](http://localhost:8000/.well-known/mcp/manifest.json)**

---

### 🧾 Using a `.env` file

You can also define overrides persistently via a `.env` file at the project root:

```env
MCP_TRANSPORT=http
MCP_HOST=0.0.0.0
MCP_PORT=8000
```

Then simply run:

```bash
docker compose up forexfactory_mcp
```

Docker Compose automatically reads `.env` and injects these variables into the container.

---

## 🧰 Makefile Targets

A `Makefile` is included to streamline common tasks and simplify Docker + MCP workflows.

| Target           | Description                                                      |
| ---------------- | ---------------------------------------------------------------- |
| `make build`     | Build the Docker image                                           |
| `make run-http`  | Run the MCP server in HTTP mode (`MCP_TRANSPORT=http`)           |
| `make run-stdio` | Run the MCP server in stdio mode for debugging                   |
| `make dev-stdio` | Start the local MCP Inspector against the stdio server           |
| `make dev-http`  | Start the Node-based MCP Inspector via `npx` against HTTP server |
| `make logs`      | Tail container logs live                                         |
| `make stop`      | Stop and remove running containers                               |

---

### Example usage

```bash
# Build Docker image
make build

# Run in stdio mode
make run-stdio

# Run in HTTP mode (for browser-based inspector)
make run-http

# Inspect local stdio server
make dev-stdio

# Inspect Dockerized HTTP server
make dev-http
```

All Makefile commands can be viewed with:

```bash
make help
```

---

### 🧩 Inspector / Debugging

Once your server is running in HTTP mode, connect with the MCP Inspector:

```bash
npx @modelcontextprotocol/inspector dev --url http://localhost:8000
```

Or for local stdio development:

```bash
uv run mcp dev src/forexfactory_mcp/main.py
```

---

### 🧹 Cleanup

To stop all running containers and remove temporary ones:

```bash
make stop
```

---

### 📦 Docker Compose Overview

```yaml
services:
  forexfactory_mcp:
    build: .
    image: forexfactory-mcp
    container_name: forexfactory-mcp
    stdin_open: true
    tty: true
    restart: unless-stopped
    ports:
      - "8000:8000"   # HTTP mode only
```

---

### ✅ Summary

| Mode                    | Recommended Command | Description                                      |
| ----------------------- | ------------------- | ------------------------------------------------ |
| **Local dev (stdio)**   | `make run-stdio`    | Runs server in stdio mode for direct MCP clients |
| **HTTP / SSE (Docker)** | `make run-http`     | Exposes HTTP API at `localhost:8000`             |
| **Inspect locally**     | `make dev-stdio`    | Launches Python MCP inspector                    |
| **Inspect via HTTP**    | `make dev-http`     | Launches Node inspector using npx                |

---

## 🧩 Troubleshooting Docker

Even though the Docker and Compose setup is designed to be plug-and-play, a few common issues can occur during development or rebuilds.
Here’s a quick reference to help you diagnose and fix them fast.

---

### 🐍 1. `uv` or dependency install fails during build

**Symptom**

```
ERROR: failed to solve: process "/bin/sh -c uv sync ..." did not complete successfully
```

**Cause**

* The base image lacks the latest `uv` binary or cached dependencies are stale.

**Fix**

```bash
docker compose build --no-cache forexfactory_mcp
```

This forces a clean rebuild of the image.

---

### ⚡ 2. Server starts but shuts down immediately

**Symptom**

```
INFO: Application startup complete.
ERROR: [Errno -2] Name or service not known
```

**Cause**

* The container is running in `stdio` mode but no MCP client is attached.
* You likely intended to run in `http` mode.

**Fix**
Use either:

```bash
make run-http
```

or manually override:

```bash
docker compose run --rm --service-ports -e MCP_TRANSPORT=http forexfactory_mcp
```

---

### 🌐 3. Port already in use (`[Errno 98] Address already in use`)

**Cause**

* Another service (or a previously running container) is already bound to port `8000`.

**Fix**

1. Stop old containers:

   ```bash
   make stop
   ```
2. Or run on a different port:

   ```bash
   docker compose run --rm --service-ports -e MCP_TRANSPORT=http -e MCP_PORT=8080 forexfactory_mcp
   ```

   Then access it via `http://localhost:8080`.

---

### 🔐 4. Playwright browser fails to start

**Symptom**

```
Error: Failed to launch browser process!
```

**Cause**

* Playwright dependencies weren’t installed correctly in the image.
* Headless Chromium requires additional libraries.

**Fix**
Rebuild the image and ensure Playwright installs correctly:

```bash
docker compose build --no-cache
docker compose run forexfactory_mcp playwright install chromium
```

---

### 🧱 5. `mcp dev` fails with “No server object found”

**Cause**

* The MCP inspector couldn’t find a global `app = FastMCP()` instance.

**Fix**
Ensure your `server.py` (or `main.py`) includes:

```python
app = FastMCP(name="forexfactory-mcp", host=host, port=port)
```

at the **top level**, not inside a function.

---

### 📦 6. `.env` changes not taking effect

**Cause**

* Docker Compose caches environment variables from a previous run.

**Fix**
Restart the service with fresh environment context:

```bash
docker compose down
docker compose up forexfactory_mcp
```

Or verify environment injection:

```bash
docker compose config
```

(Shows the final merged environment passed to each container.)

---

### 🧰 7. Viewing container logs

If your server runs in detached mode:

```bash
make logs
```

To follow logs live:

```bash
docker compose logs -f forexfactory_mcp
```

---

### 🧼 8. Cleaning up everything

If you need a full reset (containers + images + cache):

```bash
docker compose down --rmi all --volumes --remove-orphans
```

---

### ✅ Quick Checklist

| Symptom                | Likely Fix                        |
| ---------------------- | --------------------------------- |
| Server exits instantly | Switch to `MCP_TRANSPORT=http`    |
| Port 8000 busy         | Change to `MCP_PORT=8080`         |
| Logs doubled           | Add `logger.propagate = False`    |
| Browser launch fails   | Run `playwright install chromium` |
| `.env` not applied     | Restart container                 |


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
