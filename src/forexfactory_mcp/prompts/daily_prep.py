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
        name=(f"{namespace}_daily_prep" if namespace else "daily_prep"),
        description="Summarize today’s economic calendar into a trader prep note.",
    )
    async def daily_prep(style: str = "bullet points"):
        ns = namespace or "ffcal"
        resources = await app.read_resource(f"{ns}://events/today")
        events = extract_json_events(resources)
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
                    "If data is unavailable, clearly state assumptions."
                    "Explicitly state where assumptions are made vs. what comes directly from the calendar. Highlight uncertainties and data gaps clearly."
                    "At the top of the report, include a short Assumptions & Limitations section that makes explicit what is derived from the calendar feed and what is assumed."
                ),
                "resources": [f"{ns}://events/today"],
            }
        ]
