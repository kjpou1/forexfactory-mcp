# src/forexfactory_mcp/services/data_service.py

import datetime as dt
import logging
from typing import Any, Dict, List

from ..models.time_period import TimePeriod

logger = logging.getLogger(__name__)


class DataService:
    @staticmethod
    def normalize_events(
        days_array: List[Dict[str, Any]],
        time_period: TimePeriod,
        custom_start_date: str | None = None,
        custom_end_date: str | None = None,
    ) -> Dict[str, Any]:
        """Normalize raw ForexFactory daysArray → ISO dates + clean events."""

        events = []
        for day in days_array:
            for ev in day.get("events", []):
                events.append(
                    {
                        "id": ev.get("id"),
                        "title": ev.get("name"),
                        "country": ev.get("country"),
                        "currency": ev.get("currency"),
                        "impact": ev.get("impactName"),
                        "time": ev.get("timeLabel"),
                        "actual": ev.get("actual"),
                        "forecast": ev.get("forecast"),
                        "previous": ev.get("previous"),
                        "date": day.get("date"),
                        "dateiso": DataService._normalize_date(day.get("date")),
                        "dateline": day.get("dateline"),
                        "url": ev.get("url"),
                    }
                )

        start, end = DataService._date_range(
            time_period, custom_start_date, custom_end_date
        )
        return {"range": [start, end], "events": events}

    @staticmethod
    def _normalize_date(date_str: str | None) -> str | None:
        """Convert ForexFactory date strings → ISO date (YYYY-MM-DD).
        Returns None if input is None or empty.
        """
        if not date_str:
            return None

        try:
            # Strip HTML tags if present
            clean = (
                date_str.replace("<span>", " ")
                .replace("</span>", " ")
                .replace(",", "")
                .strip()
            )

            # Try formats
            formats = ["%a %b %d %Y", "%b %d %Y"]

            for fmt in formats:
                try:
                    parsed = dt.datetime.strptime(clean, fmt)
                    return parsed.date().isoformat()
                except ValueError:
                    continue

            # Handle case with no year → assume current year
            try:
                parsed = dt.datetime.strptime(clean, "%a %b %d")
                return parsed.replace(year=dt.date.today().year).date().isoformat()
            except ValueError:
                pass

            return date_str  # fallback raw
        except Exception:
            return date_str

    @staticmethod
    def _date_range(
        time_period: TimePeriod, custom_start: str | None, custom_end: str | None
    ) -> tuple[str, str]:
        today = dt.date.today()

        if time_period == TimePeriod.TODAY:
            return today.isoformat(), today.isoformat()
        elif time_period == TimePeriod.THIS_WEEK:
            start = today - dt.timedelta(days=today.weekday())
            end = start + dt.timedelta(days=6)
            return start.isoformat(), end.isoformat()
        elif time_period == TimePeriod.CUSTOM and custom_start and custom_end:
            return custom_start, custom_end
        else:
            return today.isoformat(), today.isoformat()
