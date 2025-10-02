import logging
from typing import List, Optional

from mcp.server.fastmcp import FastMCP

from forexfactory_mcp.models.time_period import TimePeriod
from forexfactory_mcp.services.ff_scraper_service import FFScraperService
from forexfactory_mcp.utils.event_utils import extract_and_normalize_events

logger = logging.getLogger(__name__)


def register_get_calendar_tool(app: FastMCP, namespace: str) -> None:
    """
    Register the get_calendar_events tool with the MCP server.
    """

    @app.tool(
        name=f"{namespace}_get_calendar_events",
        description="Retrieve ForexFactory calendar events for a given time period or custom date range."
        "Valid `time_period` values include: today, tomorrow, yesterday, "
        "this_week, next_week, last_week, this_month, next_month, last_month, custom.",
    )
    async def get_calendar_events(
        time_period: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> list[dict]:  # 👈 return JSON, not Pydantic
        """
        Parameters
        ----------
        time_period : str, optional
            Named period such as today, tomorrow, yesterday, this_week,
            next_week, last_week, this_month, next_month, last_month, custom.
        start_date : str, optional
            Start date in YYYY-MM-DD (required if time_period='custom').
        end_date : str, optional
            End date in YYYY-MM-DD (required if time_period='custom').

        Returns
        -------
        List[Event]
            List of structured calendar events.
        """

        # CASE 1: Named time period
        if time_period and time_period.lower() != "custom":
            try:
                # normalize before parsing
                normalized = time_period.strip().lower().replace(" ", "_")
                tp = TimePeriod.from_text(normalized)
            except ValueError:
                raise ValueError(
                    f"Invalid time_period '{time_period}'. "
                    f"Valid options: {', '.join([t.value for t in TimePeriod])}"
                )

            scraper = FFScraperService(time_period=tp)
            raw_events = await scraper.get_events()

        # CASE 2: Custom date range
        else:
            TimePeriod.validate_date_format(start_date)
            TimePeriod.validate_date_format(end_date)
            scraper = FFScraperService(
                time_period=TimePeriod.CUSTOM,
                custom_start_date=start_date,
                custom_end_date=end_date,
            )
            raw_events = await scraper.get_events()

        normalized = extract_and_normalize_events(raw_events)

        return normalized
