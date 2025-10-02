from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from forexfactory_mcp.utils.prompt_utils import (
    build_markdown_table,
    extract_json_events,
)


def register(app: FastMCP, namespace: str | None = None) -> None:
    @app.prompt(
        name=(f"{namespace}_daily_playbook" if namespace else "daily_playbook"),
        description=(
            "FX daily trading playbook: overnight recap, session handoff, key levels, "
            "and today’s risk events with tactical FX setups."
        ),
    )
    async def daily_playbook(style: str = "concise bullet points"):
        ns = namespace or "ffcal"
        # Pull today’s calendar to ground the risk events section
        resources = await app.read_resource(f"{ns}://events/today")
        events = extract_json_events(resources)
        md_table = build_markdown_table(events)

        return [
            {
                "role": "user",
                "content": (
                    "You are an FX macro strategist preparing a morning playbook for "
                    "professional traders ahead of London open. "
                    "Produce today’s FX trading playbook in "
                    f"{style}. Cover the following sections:\n\n"
                    "1) Overnight Recap: Asia session drivers, notable headlines, cross-asset moves.\n"
                    "2) Session Handoff: Asia → London → NY flow, expected liquidity/vol windows.\n"
                    "3) Key Levels: DXY, major FX pairs (EURUSD, GBPUSD, USDJPY, AUDUSD), and 10y UST.\n"
                    "4) Today’s Risk Events: summarize timing and relevance using the calendar below.\n"
                    "5) Tactical Setups: concrete trade ideas with triggers, invalidation, and catalysts.\n\n"
                    "Here is today’s ForexFactory calendar feed (structured):\n\n"
                    f"{md_table}\n\n"
                    "Guidelines: Be market-relevant and concise. Note expected volatility windows and "
                    "cross-asset spillovers. End with a brief risk disclaimer."
                    "If data is unavailable, clearly state assumptions."
                    "Explicitly state where assumptions are made vs. what comes directly from the calendar. Highlight uncertainties and data gaps clearly."
                    "At the top of the report, include a short Assumptions & Limitations section that makes explicit what is derived from the calendar feed and what is assumed."
                ),
                "resources": [f"{ns}://events/today"],
            }
        ]
