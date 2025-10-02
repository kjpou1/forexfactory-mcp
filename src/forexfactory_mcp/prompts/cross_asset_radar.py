from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from forexfactory_mcp.utils.prompt_utils import (
    build_markdown_table,
    extract_json_events,
)


def register(app: FastMCP, namespace: str | None = None) -> None:
    @app.prompt(
        name=(f"{namespace}_cross_asset_radar" if namespace else "cross_asset_radar"),
        description=(
            "Cluster week’s events by cross-asset spillovers (oil→CAD, gold→AUD, "
            "US yields→USD/JPY). Highlight non-FX drivers relevant to FX."
        ),
    )
    async def cross_asset_radar(style: str = "bullet points"):
        ns = namespace or "ffcal"
        # Use this week’s events for a live radar. Could be parameterized later.
        resources = await app.read_resource(f"{ns}://events/week")
        events = extract_json_events(resources)
        md_table = build_markdown_table(events)

        return [
            {
                "role": "user",
                "content": (
                    "You are an FX macro strategist building a cross-asset radar. "
                    "Cluster the week’s events by likely cross-asset spillovers and "
                    "map them to FX implications.\n\n"
                    "Examples of linkages to consider: oil→CAD/NOK, gold→AUD/NZD, "
                    "US yields→USD/JPY, European rates→EUR crosses, risk sentiment→JPY/CHF, "
                    "equities and earnings→USD, commodities→EMFX.\n\n"
                    f"Output in {style} with clear subheads: (1) Oil/Energy, (2) Metals, (3) Rates, "
                    f"(4) Equities/Risk, (5) Other Commodities/EM. For each, highlight what non-FX "
                    f"traders will watch that matters for FX, expected volatility windows, and key pairs.\n\n"
                    "Here is this week’s ForexFactory calendar feed (structured):\n\n"
                    f"{md_table}\n\n"
                    "End with a concise FX trade watchlist and a short risk disclaimer."
                    "If data is unavailable, clearly state assumptions."
                    "Explicitly state where assumptions are made vs. what comes directly from the calendar. Highlight uncertainties and data gaps clearly."
                    "At the top of the report, include a short Assumptions & Limitations section that makes explicit what is derived from the calendar feed and what is assumed."
                ),
                "resources": [f"{ns}://events/week"],
            }
        ]
