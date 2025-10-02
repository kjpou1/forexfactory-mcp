import logging

from mcp.server.fastmcp import FastMCP

from forexfactory_mcp.models.time_period import TimePeriod
from forexfactory_mcp.services.data_service import DataService
from forexfactory_mcp.services.ff_scraper_service import FFScraperService

logger = logging.getLogger(__name__)


def register(app: FastMCP, namespace: str) -> None:
    """Register all ForexFactory MCP resources under the given namespace."""

    def make_resource(
        path: str,
        period: TimePeriod,
        name: str,
        title: str,
        description: str,
        mime_type: str = "application/json",
    ):
        @app.resource(
            f"{namespace}://{path}",
            name=name,
            title=title,
            description=description,
            mime_type=mime_type,
        )
        async def _resource():
            try:
                scraper = FFScraperService(time_period=period)
                days_array = await scraper.get_events()
                return DataService.normalize_events(days_array, period)
            except Exception as e:
                logger.exception(f"⚠️ Could not fetch {path}: {e}")
                return {
                    "range": [period.value, period.value],
                    "events": [],
                    "error": str(e),
                }

    # Fixed time period resources
    make_resource(
        "events/today",
        TimePeriod.TODAY,
        "events_today",
        "Today's ForexFactory Events",
        "Economic calendar events scheduled for today.",
    )

    make_resource(
        "events/week",
        TimePeriod.THIS_WEEK,
        "events_week",
        "This Week's ForexFactory Events",
        "All economic calendar events scheduled for this week.",
    )

    make_resource(
        "events/yesterday",
        TimePeriod.YESTERDAY,
        "events_yesterday",
        "Yesterday's ForexFactory Events",
        "Economic calendar events from yesterday.",
    )

    make_resource(
        "events/next_week",
        TimePeriod.NEXT_WEEK,
        "events_next_week",
        "Next Week's ForexFactory Events",
        "All economic calendar events scheduled for next week.",
    )

    make_resource(
        "events/tomorrow",
        TimePeriod.TOMORROW,
        "events_tomorrow",
        "Tomorrow's ForexFactory Events",
        "Economic calendar events scheduled for tomorrow.",
    )

    make_resource(
        "events/this_week",
        TimePeriod.THIS_WEEK,
        "events_this_week",
        "This Week's ForexFactory Events",
        "All economic calendar events scheduled for this week.",
    )

    make_resource(
        "events/last_week",
        TimePeriod.LAST_WEEK,
        "events_last_week",
        "Last Week's ForexFactory Events",
        "All economic calendar events from last week.",
    )

    make_resource(
        "events/this_month",
        TimePeriod.THIS_MONTH,
        "events_this_month",
        "This Month's ForexFactory Events",
        "All economic calendar events scheduled for this month.",
    )

    make_resource(
        "events/next_month",
        TimePeriod.NEXT_MONTH,
        "events_next_month",
        "Next Month's ForexFactory Events",
        "All economic calendar events scheduled for next month.",
    )

    make_resource(
        "events/last_month",
        TimePeriod.LAST_MONTH,
        "events_last_month",
        "Last Month's ForexFactory Events",
        "All economic calendar events from last month.",
    )

    # Custom range
    @app.resource(f"{namespace}://events/range/{{start}}/{{end}}")
    async def events_range(start: str, end: str):
        try:
            TimePeriod.validate_date_format(start)
            TimePeriod.validate_date_format(end)
            scraper = FFScraperService(
                time_period=TimePeriod.CUSTOM,
                custom_start_date=start,
                custom_end_date=end,
            )
            days_array = await scraper.get_events()
            return DataService.normalize_events(
                days_array, TimePeriod.CUSTOM, start, end
            )
        except Exception as e:
            logger.exception(f"⚠️ Could not fetch {namespace}://events/range: {e}")
            return {"range": [start, end], "events": [], "error": str(e)}
