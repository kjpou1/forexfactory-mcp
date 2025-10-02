from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from forexfactory_mcp.utils.prompt_utils import (
    build_markdown_table,
    extract_json_events,
)


def register(app: FastMCP, namespace: str | None = None) -> None:
    @app.prompt(
        name=(f"{namespace}_positioning_flow_note" if namespace else "positioning_flow_note"),
        description=(
            "Summarize CFTC positioning, ETF flows, and key options expiries overlapping "
            "macro events; highlight where positioning may amplify volatility."
        ),
    )
    async def positioning_flow_note(style: str = "concise bullet points"):
        ns = namespace or "ffcal"
        # Calendar context helps identify overlaps with macro events. Using this week.
        resources = await app.read_resource(f"{ns}://events/week")
        events = extract_json_events(resources)
        md_table = build_markdown_table(events)

        return [
            {
                "role": "user",
                "content": (
                    "You are an FX macro strategist producing a positioning & flow note. "
                    "Fetch the *latest* CFTC Commitment of Traders (futures-only, non-commercial), "
                    "ETF/fund flow data (currency, commodity-linked, EM), "
                    "and FX options expiry boards (CME/DTCC strike clusters). "
                    "Summarize them in sections:\n"
                    "1) CFTC positioning (net specs, gross longs/shorts, WoW change, 52w percentile)\n"
                    "2) ETF/flow color (in/out by region/theme)\n"
                    "3) Options expiries (strikes, notional, timing)\n"
                    "4) Overlap map vs this week’s calendar\n"
                    "5) Implications & trade bias.\n\n"
                    "Use the calendar feed below to anchor overlaps:\n\n"
                    f"{md_table}\n\n"
                    "End with a risk disclaimer. "
                    "If data is unavailable, clearly state assumptions."
                    "Explicitly state where assumptions are made vs. what comes directly from the calendar. Highlight uncertainties and data gaps clearly."
                    "At the top of the report, include a short Assumptions & Limitations section that makes explicit what is derived from the calendar feed and what is assumed."
                ),
                "resources": [f"{ns}://events/week"],
            }
        ]
