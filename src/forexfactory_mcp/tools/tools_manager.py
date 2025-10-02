import logging

from mcp.server.fastmcp import FastMCP

from forexfactory_mcp.tools.get_calendar_tool import register_get_calendar_tool

logger = logging.getLogger(__name__)


def register_tools(app: FastMCP, namespace: str) -> None:
    """
    Register all available MCP tools here.
    """
    logger.info("Registering MCP tools...")

    # Add tools here
    register_get_calendar_tool(app, namespace)

    logger.info("All tools registered.")
