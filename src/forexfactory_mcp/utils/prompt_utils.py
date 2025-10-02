# src/forexfactory_mcp/prompts.py
"""
ForexFactory MCP Prompts
------------------------

This module defines reusable MCP prompts that LLM clients can call by name.
Prompts are higher-level "templates" for conversations: they bundle instructions
(system + user messages) and optionally reference resources (URIs like
`ffcal://events/today`) that supply structured data to the model.

The prompts here are designed for FX traders:
- ffcal_daily_prep: Summarize today’s events for day trading.
- ffcal_weekly_outlook: Summarize high-impact events for the upcoming week.
"""

from __future__ import annotations

import json
import logging
from typing import Any, Iterable

from mcp.server.fastmcp import FastMCP

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def extract_json_events(resources: Iterable[Any]) -> list[dict]:
    """Extract JSON event data from resource blocks."""
    events: list[dict] = []
    for block in resources:
        if block.mime_type == "application/json":
            try:
                data = json.loads(block.content)
                events.extend(data.get("events", []))
            except Exception as e:
                logger.warning(f"Could not parse JSON block: {e}")
        elif block.mime_type == "text/plain":
            logger.debug("Plain text block found, skipping JSON parse.")
    return events


def build_markdown_table(events: list[dict]) -> str:
    """Format a list of events into a Markdown table."""
    header = (
        "| Date | Time | Currency | Event | Impact | Forecast | Actual | Previous |\n"
        "|------|------|----------|-------|--------|----------|--------|----------|\n"
    )
    rows = []
    for e in events:
        rows.append(
            f"| {e.get('dateiso','')} "
            f"| {e.get('time','')} "
            f"| {e.get('currency','')} "
            f"| {e.get('title','')} "
            f"| {e.get('impact','')} "
            f"| {e.get('forecast','')} "
            f"| {e.get('actual','')} "
            f"| {e.get('previous','')} |"
        )
    return header + "\n".join(rows)


# ---------------------------------------------------------------------------
# Prompt registration
# ---------------------------------------------------------------------------


def register(app: FastMCP) -> None:
    """Register all ForexFactory prompts with the given FastMCP app."""

    @app.prompt(
        name="ffcal_daily_prep",
        description="Summarize today’s economic calendar into a trader prep note.",
    )
    async def ffcal_daily_prep(style: str = "bullet points"):
        resources = await app.read_resource("ffcal://events/today")
        events = extract_json_events(resources)

        # For daily, include all events (not just high-impact)
        md_table = build_markdown_table(events)

        return [
            {
                "role": "user",
                "content": (
                    "You are an FX macro day-trader’s assistant. "
                    "Summarize only the *market-relevant* items and times. "
                    "Highlight high-impact events, expected volatility windows, "
                    "and any clusters by currency.\n\n"
                    "Here is today’s ForexFactory calendar feed:\n\n"
                    f"{md_table}\n\n"
                    f"Output as {style}. Include a short risk disclaimer at the end."
                ),
                "resources": ["ffcal://events/today"],
            }
        ]

    @app.prompt(
        name="ffcal_weekly_outlook",
        description="Summarize high-impact economic events for the upcoming week.",
    )
    async def ffcal_weekly_outlook(style: str = "summary"):
        resources = await app.read_resource("ffcal://events/week")
        events = extract_json_events(resources)

        # Filter only high-impact
        md_table = build_markdown_table(events)

        return [
            {
                "role": "user",
                "content": (
                    "You are an FX macro strategist. Summarize only the *high-impact* "
                    "economic events for the upcoming week. Cluster events by theme "
                    "(inflation, employment, central bank) and currency. Highlight "
                    "potential volatility windows and cross-asset spillovers "
                    "(rates, equities, commodities, FX).\n\n"
                    "Here is this week’s ForexFactory calendar feed:\n\n"
                    f"{md_table}\n\n"
                    f"Output as a {style}. End with a watchlist by currency and "
                    f"include a short risk disclaimer at the end."
                ),
                "resources": ["ffcal://events/week"],
            }
        ]
