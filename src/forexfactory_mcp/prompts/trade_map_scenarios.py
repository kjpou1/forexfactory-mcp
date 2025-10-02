from __future__ import annotations

from mcp.server.fastmcp import FastMCP


def register(app: FastMCP, namespace: str | None = None) -> None:
    @app.prompt(
        name=(f"{namespace}_trade_map_scenarios" if namespace else "trade_map_scenarios"),
        description=(
            "For a chosen event, outline upside/inline/downside scenarios with bias for USD, equities, "
            "yields, and concrete FX trade ideas."
        ),
    )
    async def trade_map_scenarios(
        event: str,
        style: str = "concise bullet points",
    ):
        return [
            {
                "role": "user",
                "content": (
                    "You are an FX macro strategist creating a scenario trade map. "
                    f"Event: {event}.\n\n"
                    f"Outline three scenarios in {style}:\n"
                    "1) Upside surprise\n"
                    "2) Inline/consensus\n"
                    "3) Downside surprise\n\n"
                    "For each scenario, provide:\n"
                    "- Directional bias: USD, equities, rates/yields\n"
                    "- FX trade ideas: specific pairs with triggers, invalidation, and catalysts\n"
                    "- Expected volatility window and confidence\n\n"
                    "Add a brief note on positioning/flows if relevant (squeezes vs follow-through). "
                    "End with a short risk disclaimer."
                    "If data is unavailable, clearly state assumptions."
                    "Explicitly state where assumptions are made vs. what comes directly from the calendar. Highlight uncertainties and data gaps clearly."
                    "At the top of the report, include a short Assumptions & Limitations section that makes explicit what is derived from the calendar feed and what is assumed."
                ),
            }
        ]
