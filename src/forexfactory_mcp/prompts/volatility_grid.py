from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from forexfactory_mcp.utils.prompt_utils import (
    build_markdown_table,
    extract_json_events,
)


def register(app: FastMCP, namespace: str | None = None) -> None:
    @app.prompt(
        name=(f"{namespace}_volatility_grid" if namespace else "volatility_grid"),
        description=(
            "Heatmap of weekly event risk: x-axis time zones (Asia/London/NY), "
            "y-axis days; bold high-impact; note vol clustering."
        ),
    )
    async def volatility_grid(style: str = "markdown table"):
        ns = namespace or "ffcal"
        # Use this week’s events
        resources = await app.read_resource(f"{ns}://events/week")
        events = extract_json_events(resources)
        md_table = build_markdown_table(events)

        return [
            {
                "role": "user",
                "content": (
                    "Build a volatility heatmap for this week’s event risk. "
                    "Lay out a grid with x-axis = time zones (Asia, London, NY) and "
                    "y-axis = days (Mon→Fri). Mark high-impact events in bold. "
                    "Use the calendar feed below:\n\n"
                    f"{md_table}\n\n"
                    "Call out expected volatility clusters and narrow windows for breaks.\n\n"
                    f"Return the grid as a {style}. Keep it compact and trader-friendly. "
                    "Under the grid, add 3-5 bullets on the biggest clustering windows and likely FX implications."
                    "End with a risk disclaimer. "
                    "If data is unavailable, clearly state assumptions."
                    "Explicitly state where assumptions are made vs. what comes directly from the calendar. Highlight uncertainties and data gaps clearly."
                    "At the top of the report, include a short Assumptions & Limitations section that makes explicit what is derived from the calendar feed and what is assumed."
                ),
                "resources": [f"{ns}://events/week"],
            }
        ]
