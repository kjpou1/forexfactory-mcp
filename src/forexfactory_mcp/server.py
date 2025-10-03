# src/forexfactory_mcp/main.py

import argparse
import asyncio
import logging
import sys

from mcp.server.fastmcp import FastMCP

from forexfactory_mcp.prompts.prompt_manager import register as register_prompts
from forexfactory_mcp.resources.resource_manager import register as register_resources
from forexfactory_mcp.settings import get_settings
from forexfactory_mcp.tools.tools_manager import register_tools

# -----------------------------------------------------------------------------
# Logging setup
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
# CLI args
# -----------------------------------------------------------------------------
def parse_arguments():
    parser = argparse.ArgumentParser(description="ForexFactory MCP Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "http", "sse"],
        default="stdio",
        help="Transport method for the MCP server (default: stdio)",
    )
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host to bind (http/sse only, default 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind (http/sse only, default 8000)",
    )
    return parser.parse_args()


# -----------------------------------------------------------------------------
# App setup
# -----------------------------------------------------------------------------
def setup_app(app):
    """Register resources, prompts, and tools."""
    settings = get_settings()
    register_resources(app, settings.NAMESPACE)
    register_prompts(app, settings.NAMESPACE)
    register_tools(app, settings.NAMESPACE)
    logger.info("✅ ForexFactory MCP server started, waiting for client…")


# -----------------------------------------------------------------------------
# Entrypoint
# -----------------------------------------------------------------------------
if __name__ == "__main__":

    settings = get_settings()

    args = parse_arguments()

    # Resolve precedence: CLI > .env > defaults
    transport = args.transport or settings.MCP_TRANSPORT
    host = args.host or settings.MCP_HOST
    port = args.port or settings.MCP_PORT

    # configure app with host/port here
    app = FastMCP(
        name="forexfactory-mcp",
        host=host,
        port=port,
    )
    setup_app(app)

    try:
        if transport == "stdio":
            asyncio.run(app.run_stdio_async())

        elif transport == "http":
            asyncio.run(app.run_streamable_http_async())

        elif transport == "sse":
            logger.warning(
                "⚠️ SSE transport is deprecated. Consider using HTTP instead."
            )
            asyncio.run(app.run_sse_async())

    except KeyboardInterrupt:
        logger.info("🛑 Server interrupted and shutting down...")
    except Exception as e:
        print(f"Error starting MCP server: {e}")
        if args.transport in ["http", "sse"]:
            print(f"Configured host/port: {args.host}:{args.port}")
            print("Common fixes:")
            print(f"1. Ensure port {args.port} is available")
            print(f"2. Check if another service is bound")
            print("3. Try a different port with --port <PORT>")
        sys.exit(1)
        sys.exit(1)
        sys.exit(1)
