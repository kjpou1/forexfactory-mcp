# ─────────────────────────────────────────────────────────────────────────────
# 📜 ForexFactory MCP Server – Main Entrypoint
#
# This file launches the ForexFactory MCP server using the FastMCP framework.
# It supports multiple transports (stdio, http, sse) and allows command-line
# overrides of host and port parameters.
#
# Usage Examples:
#   • Local dev inspector:
#       uv run mcp dev src/forexfactory_mcp/main.py
#
#   • Run manually (HTTP mode):
#       uv run python src/forexfactory_mcp/main.py --transport http --host 0.0.0.0 --port 8000
#
#   • Run in Docker:
#       docker compose up forexfactory_mcp
#
# This module exposes a global `app = FastMCP(...)` object so that
# `mcp dev` and MCP inspectors can automatically discover the MCP server.
# ─────────────────────────────────────────────────────────────────────────────

import argparse
import asyncio
import logging
import sys

from mcp.server.fastmcp import FastMCP

# Local modules – managers that register resources, tools, and prompts.
from forexfactory_mcp.prompts.prompt_manager import register as register_prompts
from forexfactory_mcp.resources.resource_manager import register as register_resources
from forexfactory_mcp.settings import get_settings
from forexfactory_mcp.tools.tools_manager import register_tools

# -----------------------------------------------------------------------------
# 🪵 Logging setup
# -----------------------------------------------------------------------------
logger = logging.getLogger("forexfactory-mcp")
handler = logging.StreamHandler(sys.stderr)
formatter = logging.Formatter(
    "[%(asctime)s] %(levelname)-8s %(message)s %(filename)s:%(lineno)d",
    datefmt="%m/%d/%y %H:%M:%S",
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


# -----------------------------------------------------------------------------
# ⚙️ CLI argument parsing
# -----------------------------------------------------------------------------
def parse_arguments():
    """
    Parse command-line arguments for transport, host, and port.
    Allows MCP CLI or Docker to override defaults defined in settings.py.
    Uses parse_known_args() to ignore any extra flags passed by `mcp dev`.
    """
    parser = argparse.ArgumentParser(description="ForexFactory MCP Server")

    parser.add_argument(
        "--transport",
        choices=["stdio", "http", "sse"],
        default=None,
        help="Transport method for the MCP server (default: stdio)",
    )
    parser.add_argument(
        "--host",
        type=str,
        default=None,
        help="Host to bind (http/sse only, default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=None,
        help="Port to bind (http/sse only, default: 8000)",
    )

    # 👇 Allow MCP CLI to pass its own args without breaking argparse
    _args, _unknown = parser.parse_known_args()
    return _args


# -----------------------------------------------------------------------------
# 🧩 App setup helper
# -----------------------------------------------------------------------------
def setup_app(_app):
    """
    Register all resources, prompts, and tools with the FastMCP app.
    This ensures that the server exposes the full MCP API surface.
    """
    register_resources(_app, settings.NAMESPACE)
    register_prompts(_app, settings.NAMESPACE)
    register_tools(_app, settings.NAMESPACE)


# -----------------------------------------------------------------------------
# 🔧 Resolve configuration (CLI > ENV > defaults)
# -----------------------------------------------------------------------------
args = parse_arguments()
settings = get_settings()

transport = args.transport or settings.MCP_TRANSPORT
host = args.host or settings.MCP_HOST
port = args.port or settings.MCP_PORT

# -----------------------------------------------------------------------------
# 🚀 Create global FastMCP app (required for MCP Inspector discovery)
# -----------------------------------------------------------------------------
app = FastMCP(
    name="forexfactory-mcp",
    host=host,
    port=port,
)

setup_app(app)


# -----------------------------------------------------------------------------
# 🔄 Async Entrypoint
# -----------------------------------------------------------------------------
async def main_async():
    """
    Main async entrypoint that starts the MCP server with the chosen transport.
    Supports stdio (local dev), HTTP (Docker/remote), and SSE (legacy).
    """
    logger.info(f"🚀 Starting ForexFactory MCP server (transport={transport})")

    try:
        if transport == "stdio":
            # Standard input/output transport for local inspectors
            await app.run_stdio_async()

        elif transport == "http":
            # Streamable HTTP mode (recommended for Docker/production)
            await app.run_streamable_http_async()

        elif transport == "sse":
            # Legacy Server-Sent Events transport (deprecated)
            logger.warning(
                "⚠️ SSE transport is deprecated. Consider using HTTP instead."
            )
            await app.run_sse_async()

        else:
            raise ValueError(f"Unknown transport: {transport}")

    except KeyboardInterrupt:
        logger.info("🛑 Server interrupted and shutting down...")

    except Exception as e:
        # User-friendly diagnostics for common startup errors
        print(f"❌ Error starting MCP server: {e}")
        if transport in ["http", "sse"]:
            print(f"Configured host/port: {host}:{port}")
            print("Common fixes:")
            print(f"1. Ensure port {port} is available.")
            print("2. Check if another service is already bound.")
            print("3. Try a different port with --port <PORT>.")
        sys.exit(1)


# -----------------------------------------------------------------------------
# 🏁 Entrypoint wrapper
# -----------------------------------------------------------------------------
def main():
    """Entrypoint wrapper for synchronous execution (used by __main__)."""
    asyncio.run(main_async())


# -----------------------------------------------------------------------------
# 🔥 Script entrypoint
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
