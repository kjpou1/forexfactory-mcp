import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from playwright.async_api import async_playwright

from forexfactory_mcp.models.time_period import TimePeriod
from forexfactory_mcp.settings import get_settings

logger = logging.getLogger(__name__)


class FFScraperService:
    """
    Service for scraping the ForexFactory calendar using Playwright.

    This class is initialized with either:
      - A predefined TimePeriod (e.g. TODAY, NEXT_WEEK, THIS_MONTH), or
      - TimePeriod.CUSTOM with explicit start and end dates.

    Based on these parameters, the service builds the correct ForexFactory URL
    and fetches events from the calendar page by executing JavaScript in the DOM.

    Attributes
    ----------
    settings : object
        Project settings including BASE_URL, scraper timeouts, and HTTP headers.
    time_period : TimePeriod
        Enum value specifying which calendar period to fetch.
    custom_start_date : Optional[str]
        Start date string (YYYY-MM-DD) if using TimePeriod.CUSTOM.
    custom_end_date : Optional[str]
        End date string (YYYY-MM-DD) if using TimePeriod.CUSTOM.
    url : str
        Fully resolved ForexFactory calendar URL for the requested range.
    """

    def __init__(
        self,
        time_period: TimePeriod,
        custom_start_date: Optional[str] = None,
        custom_end_date: Optional[str] = None,
    ):
        """
        Initialize the scraper service.

        Parameters
        ----------
        time_period : TimePeriod
            Predefined period or CUSTOM for explicit date range.
        custom_start_date : Optional[str], default=None
            Start date (YYYY-MM-DD) if using CUSTOM.
        custom_end_date : Optional[str], default=None
            End date (YYYY-MM-DD) if using CUSTOM.
        """
        self.settings = get_settings()
        self.time_period = time_period
        self.custom_start_date = custom_start_date
        self.custom_end_date = custom_end_date
        self.url = self._build_url()

    def _format_date(self, date_str: str) -> str:
        """
        Convert YYYY-MM-DD into ForexFactory URL format (e.g., 'Sep26.2025' → 'sep26.2025').

        Parameters
        ----------
        date_str : str
            Date in YYYY-MM-DD format.

        Returns
        -------
        str
            Date string formatted for ForexFactory URL.
        """
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%b%d.%Y").lower()

    def _build_url(self) -> str:
        """
        Construct the ForexFactory calendar URL based on the time period.

        - For CUSTOM: Builds `/calendar?range=start-end`.
        - For other periods: Uses TimePeriod.to_href() mapping.

        Returns
        -------
        str
            Fully constructed calendar URL.
        """
        base_url = self.settings.BASE_URL

        if (
            self.time_period == TimePeriod.CUSTOM
            and self.custom_start_date
            and self.custom_end_date
        ):
            start_date = self._format_date(self.custom_start_date)
            end_date = self._format_date(self.custom_end_date)
            href = f"{TimePeriod.to_href(self.time_period)}{start_date}-{end_date}"
        else:
            href = TimePeriod.to_href(self.time_period)

        return f"{base_url}{href}"

    async def get_events(self) -> List[Dict[str, Any]]:
        """
        Public entry point to fetch events.

        Returns
        -------
        List[Dict[str, Any]]
            A list of normalized ForexFactory events grouped by days.
        """
        return await self._get_calendar(self.url)

    async def _get_calendar(self, url: str) -> List[Dict[str, Any]]:
        """
        Perform the actual scraping using Playwright.

        Steps:
        - Launch headless Chromium.
        - Navigate to the ForexFactory calendar URL.
        - Evaluate `window.calendarComponentStates` in the DOM.
        - Return the extracted array of days/events.

        Parameters
        ----------
        url : str
            The ForexFactory calendar URL to scrape.

        Returns
        -------
        List[Dict[str, Any]]
            Raw event data as extracted from the client-side JS object.
        """
        logger.info(f"🌐 Scraping ForexFactory: {url}")

        days_array: List[Dict[str, Any]] = []

        # Playwright session objects
        playwright = None
        browser = None
        context = None
        page = None

        timeout_ms = self.settings.SCRAPER_TIMEOUT_MS
        logger.info(f"⏱ Using timeout {timeout_ms}ms")

        try:
            # Start Playwright engine
            playwright = await async_playwright().start()
            browser = await playwright.chromium.launch(
                headless=True, args=["--no-sandbox"]
            )
            context = await browser.new_context()
            page = await context.new_page()

            # Apply timeouts
            page.set_default_timeout(timeout_ms)
            page.set_default_navigation_timeout(timeout_ms)

            # Apply extra headers and navigate
            await page.set_extra_http_headers(self.settings.extra_http_headers)
            await page.goto(url, wait_until="domcontentloaded")

            try:
                # Evaluate JS global to extract calendar state
                data = await page.evaluate(
                    """() => {
                        if (typeof window.calendarComponentStates === 'undefined') { return [] }
                        return (window.calendarComponentStates[1]?.days 
                                    || window.calendarComponentStates[0]?.days || []);
                    }"""
                )
                days_array = data or []
            except Exception as e:
                logger.error(f"⚠️ Failed to evaluate calendar state: {e}")

        except Exception as e:
            logger.exception(f"⚠️ Could not scrape ForexFactory: {e}")

        finally:
            # Always close resources in reverse order
            for obj, close_fn in [
                (page, page.close if page else None),
                (context, context.close if context else None),
                (browser, browser.close if browser else None),
                (playwright, playwright.stop if playwright else None),
            ]:
                if close_fn:
                    try:
                        await close_fn()
                    except Exception:
                        pass

        # logger.info(f"✅ Extracted {len(days_array)} days of events")
        return days_array
