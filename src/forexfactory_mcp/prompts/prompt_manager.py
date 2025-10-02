from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from forexfactory_mcp.prompts.cross_asset_radar import register as register_cross_asset
from forexfactory_mcp.prompts.daily_playbook import register as register_playbook
from forexfactory_mcp.prompts.daily_prep import register as register_daily
from forexfactory_mcp.prompts.positioning_flow_note import (
    register as register_positioning_flow,
)
from forexfactory_mcp.prompts.trade_map_scenarios import register as register_trade_map
from forexfactory_mcp.prompts.volatility_grid import register as register_vol_grid
from forexfactory_mcp.prompts.weekly_outlook import register as register_weekly
from forexfactory_mcp.prompts.weekly_outlook_next_week import (
    register as register_weekly_next,
)


def register(app: FastMCP, namespace: str | None = None) -> None:
    """Register all prompt modules with the FastMCP app.

    This function imports individual prompt registration functions from
    the `forexfactory_mcp.prompts` package and invokes them to attach
    prompts to the provided app instance.
    """

    register_daily(app, namespace)
    register_weekly(app, namespace)
    register_playbook(app, namespace)
    register_weekly_next(app, namespace)
    register_cross_asset(app, namespace)
    register_positioning_flow(app, namespace)
    register_vol_grid(app, namespace)
    register_trade_map(app, namespace)
