from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from forexfactory_mcp.utils.prompt_utils import (
    build_markdown_table,
    extract_json_events,
)


def register(app: FastMCP, namespace: str | None = None) -> None:
    @app.prompt(
        name=(f"{namespace}_weekly_outlook_next_week" if namespace else "weekly_outlook_next_week"),
        description=(
            "Sunday note: summarize next week’s macro events by theme and currency, "
            "with expected volatility windows and cross-asset spillovers."
        ),
    )
    async def weekly_outlook_next_week(style: str = "executive summary"):
        ns = namespace or "ffcal"
        # Use next week’s calendar resource as requested
        resources = await app.read_resource(f"{ns}://events/next_week")
        events = extract_json_events(resources)
        md_table = build_markdown_table(events)

        return [
            {
                "role": "user",
                "content": (
                    "You are an FX macro strategist writing a Sunday weekly outlook. "
                    "Summarize next week’s macro events by theme (inflation, employment, central banks) "
                    "and by currency. Highlight likely volatility windows and spillovers to rates, "
                    "equities, and commodities.\n\n"
                    f"Present the analysis as an {style}. Start with a high-level market bias, then sections by theme and currency. "
                    f"End with a tactical watchlist for swing trades and a short risk disclaimer.\n\n"
                    "Here is next week’s ForexFactory calendar feed (structured):\n\n"
                    f"{md_table}\n\n"
                    "End with a risk disclaimer. "
                    "If data is unavailable, clearly state assumptions."
                    "Explicitly state where assumptions are made vs. what comes directly from the calendar. Highlight uncertainties and data gaps clearly."
                    "At the top of the report, include a short Assumptions & Limitations section that makes explicit what is derived from the calendar feed and what is assumed."
                ),
                "resources": [f"{ns}://events/next_week"],
            }
        ]
