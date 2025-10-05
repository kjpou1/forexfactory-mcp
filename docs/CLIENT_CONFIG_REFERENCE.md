# 🧩 Client Configuration Reference

This document explains how to connect different **clients** — such as **Claude Desktop**, **VS Code**, and the **MCP Inspector** — to the **ForexFactory MCP Server**.

Each setup enables your client to use the server’s tools, resources, and prompts (for example, `ffcal_get_calendar_events`) directly within your workflow or chat environment.

---

## 📍 Overview

| Client                    | Connection Type  | Status        | Notes                          |
| ------------------------- | ---------------- | ------------- | ------------------------------ |
| **Claude Desktop**        | `stdio`          | ✅ Supported   | Local or Docker setup          |
| **VS Code MCP Extension** | `stdio` / `http` | 🔜 Coming soon | Similar config pattern         |
| **MCP Inspector (Node)**  | `http`           | ✅ Supported   | For debugging & visual testing |

---

## 💻 Claude Desktop (macOS)

Claude Desktop uses a JSON configuration file to discover local MCP servers:

```
~/Library/Application Support/Claude/claude_desktop_config.json
```

You can find prebuilt configuration templates in this repository:

```
client_configs/claude/
├── claude_desktop_config.json
└── claude_desktop_config_docker.json
```

Use either **local uv** or **Docker-based** setups depending on your workflow.

---

### 🧩 Option 1 — Local `uv` Setup (Direct Execution)

Copy the content of
[`client_configs/claude/claude_desktop_config.json`](../client_configs/claude/claude_desktop_config.json)
into your Claude Desktop configuration file.

```json
{
  "mcpServers": {
    "forexfactory_mcp": {
      "type": "stdio",
      "command": "/Users/YOUR_USERNAME/.local/bin/uv",
      "args": [
        "--directory",
        "/PATH/TO/YOUR/forexfactory-mcp/",
        "run",
        "ffcal-server"
      ]
    }
  }
}
```

#### 🧠 Replace These Placeholders

| Placeholder                          | Replace With          | How to Find               |
| ------------------------------------ | --------------------- | ------------------------- |
| `YOUR_USERNAME`                      | your macOS username   | `echo $USER`              |
| `/PATH/TO/YOUR/forexfactory-mcp/`    | absolute path to repo | drag folder into Terminal |
| `/Users/YOUR_USERNAME/.local/bin/uv` | full path to `uv`     | `which uv`                |

#### ✅ Example (Mac)

```json
{
  "mcpServers": {
    "forexfactory_mcp": {
      "type": "stdio",
      "command": "/Users/egodraconis/.local/bin/uv",
      "args": [
        "--directory",
        "/Users/Jimmy/websharp/projects/python/ai/agents/mcp/mcp-servers/forexfactory-mcp/",
        "run",
        "ffcal-server"
      ]
    }
  }
}
```

This setup runs the MCP server directly from your local environment — ideal for **development** and **rapid iteration**.

---

### 🐳 Option 2 — Docker Setup (Recommended for Isolation)

If you prefer not to manage dependencies locally, use Docker for a sandboxed, reproducible setup.

Use the config provided at
[`client_configs/claude/claude_desktop_config_docker.json`](../client_configs/claude/claude_desktop_config_docker.json):

```json
{
  "mcpServers": {
    "forexfactory_mcp": {
      "type": "stdio",
      "command": "docker",
      "args": [
        "compose",
        "run",
        "--rm",
        "forexfactory_mcp"
      ]
    }
  }
}
```

#### ⚙️ Build the Docker Image First

Before launching Claude:

```bash
# Using Makefile
make build

# Or directly
docker compose build
```

> 🧾 The Docker setup runs the same MCP server inside a container.
> It automatically loads your `.env` file and matches the `forexfactory_mcp` service name in your `docker-compose.yml`.

#### 🧩 Notes

| Behavior           | Description                                      |
| ------------------ | ------------------------------------------------ |
| `--rm`             | Cleans up the container automatically after exit |
| `forexfactory_mcp` | Must match your Docker service name              |
| `.env`             | Loaded automatically from project root           |
| Logs               | Stream into Claude’s console                     |
| Dependencies       | Fully isolated from your system Python           |

> 💡 *You can keep both local and Docker configurations in your Claude file — rename one key (e.g., `forexfactory_mcp_docker`) and toggle as needed.*

---

### 🔍 Testing Your Setup

After saving and restarting Claude Desktop, ask:

> “List all available MCP tools and describe what each does.”

#### ✅ Expected Result

```
I have access to one MCP (Model Context Protocol) tool:

ForexFactory Calendar Tool:
- forexfactory_mcp:ffcal_get_calendar_events - Retrieves ForexFactory calendar events for economic news and data releases

This tool allows me to fetch forex/economic calendar events for various time periods including:
- Predefined periods: today, tomorrow, yesterday, this_week, next_week, last_week, this_month, next_month, last_month
- Custom date ranges (by specifying start_date and end_date)
```

---

### 🧰 Troubleshooting Claude Desktop

| Symptom                          | Likely Cause                 | Fix                                           |
| -------------------------------- | ---------------------------- | --------------------------------------------- |
| **No tools listed**              | Invalid JSON or wrong path   | Validate JSON and restart Claude              |
| **Command not found: uv/docker** | Path or missing installation | Run `which uv` or `docker info`               |
| **Server exits instantly**       | Wrong directory path         | Ensure repo path ends in `/forexfactory-mcp/` |
| **Claude hangs**                 | Playwright cold start        | Wait 10–15s or prebuild Docker image          |

---

### ✅ Summary of Claude Desktop Options

| Mode           | Config File                         | Command                                    | Description               | Recommended Use          |
| -------------- | ----------------------------------- | ------------------------------------------ | ------------------------- | ------------------------ |
| **Local (uv)** | `claude_desktop_config.json`        | `/Users/.../uv run ffcal-server`           | Fast and local            | Development              |
| **Docker**     | `claude_desktop_config_docker.json` | `docker compose run --rm forexfactory_mcp` | Isolated and reproducible | Production or sandboxing |

---

## 🧠 Visual Studio Code (Coming Soon)

Future versions of the VS Code MCP extension will support both `stdio` and `http` transports.

Configuration will be similar to Claude Desktop but saved under:

```
.vscode/mcp.config.json
```

Example (planned):

```json
{
  "servers": {
    "forexfactory_mcp": {
      "transport": "http",
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

> 🔜 Once official MCP extension support stabilizes, this section will include tested JSON templates under `client_configs/vscode/`.

---

## 🧪 MCP Inspector (Web Debugging)

To visually inspect the ForexFactory MCP server’s tools, resources, and prompts:

### 1️⃣ Start the Server

```bash
uv run ffcal-server --transport http --host 0.0.0.0 --port 8000
```

### 2️⃣ Launch the Inspector

```bash
npx @modelcontextprotocol/inspector dev --url http://localhost:8000
```

You should see:

* **Tools** → `ffcal_get_calendar_events`
* **Resources** → `ffcal://events/today`, `ffcal://events/week`, etc.
* **Prompts** → `ffcal_weekly_outlook`, `ffcal_volatility_grid`, etc.

---

## 🔗 Official References

* 🏠 [Connecting Local MCP Servers](https://modelcontextprotocol.io/docs/develop/connect-local-servers)
* 🌐 [Connecting Remote MCP Servers](https://modelcontextprotocol.io/docs/develop/connect-remote-servers)

---

## ✅ Quick Checklist

| Step | Action                                | Expected Result                      |
| ---- | ------------------------------------- | ------------------------------------ |
| 1️⃣    | Add Claude config (local or docker)   | Claude recognizes `forexfactory_mcp` |
| 2️⃣    | Build Docker image if using container | Image builds successfully            |
| 3️⃣    | Restart Claude                        | MCP server handshake confirmed       |
| 4️⃣    | Ask “List all MCP tools”              | Lists `ffcal_get_calendar_events`    |
| 5️⃣    | Call tool                             | Returns ForexFactory calendar data   |

