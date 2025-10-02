# src/forexfactory_mcp/main.py

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
# MCP App
# -----------------------------------------------------------------------------
app = FastMCP(name="forexfactory-mcp")

settings = get_settings()


def setup_app():
    """Register resources and prompts."""
    # Register ForexFactory calendar resources (today, week, etc.)
    register_resources(app, settings.NAMESPACE)

    register_prompts(app, settings.NAMESPACE)

    register_tools(app, settings.NAMESPACE)

    logger.info("✅ ForexFactory MCP server started, waiting for client…")


# -----------------------------------------------------------------------------
# Entrypoint
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    setup_app()
    try:
        app.run(transport="stdio")
    except KeyboardInterrupt:
        logger.info("🛑 Server interrupted and shutting down...")
