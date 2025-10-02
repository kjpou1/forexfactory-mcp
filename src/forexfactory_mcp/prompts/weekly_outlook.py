from __future__ import annotations

import logging

from mcp.server.fastmcp import FastMCP

from forexfactory_mcp.utils.prompt_utils import (
    build_markdown_table,
    extract_json_events,
)

logger = logging.getLogger(__name__)


def register(app: FastMCP, namespace: str | None = None) -> None:
    @app.prompt(
        name=(f"{namespace}_weekly_outlook" if namespace else "weekly_outlook"),
        description="Summarize high-impact economic events for the upcoming week.",
    )
    async def weekly_outlook(style: str = "summary"):
        ns = namespace or "ffcal"
        resources = await app.read_resource(f"{ns}://events/week")
        events = extract_json_events(resources)
        # No high-impact filtering per request; include all events
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
                    f"Output as a {style}. End with a watchlist by currency."
                    "End with a risk disclaimer. "
                    "If data is unavailable, clearly state assumptions."
                    "Explicitly state where assumptions are made vs. what comes directly from the calendar. Highlight uncertainties and data gaps clearly."
                    "At the top of the report, include a short Assumptions & Limitations section that makes explicit what is derived from the calendar feed and what is assumed."
                ),
                "resources": [f"{ns}://events/week"],
            }
        ]
