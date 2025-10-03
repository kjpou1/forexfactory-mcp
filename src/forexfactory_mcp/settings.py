"""
settings.py

Centralized application configuration for ForexFactory MCP.

This module uses Pydantic's BaseSettings to define strongly-typed configuration
values with sensible defaults. Environment variables (and .env files) override
these defaults automatically.

We also expose a `get_settings()` function (cached with @lru_cache) to ensure
the Settings object is created only once per process. This avoids the pitfalls
of manual globals or singletons while keeping access simple and consistent.

Usage:
    from forexfactory_mcp.settings import get_settings

    settings = get_settings()
    print(settings.BASE_URL)
    timeout = settings.SCRAPER_TIMEOUT_MS
    headers = settings.EXTRA_HTTP_HEADERS
"""

from functools import lru_cache
from typing import List, Optional
from zoneinfo import ZoneInfo

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from tzlocal import get_localzone


class Settings(BaseSettings):
    """
    Application configuration class.

    Values are:
      - Pulled from environment variables if available.
      - Otherwise, fallback defaults defined here are used.
      - Optionally loaded from a `.env` file in the project root.

    Example:
        export SCRAPER_TIMEOUT_MS=10000
        → overrides default timeout (5s → 10s).
    """

    # === Core configuration values ===
    BASE_URL: str = "https://www.forexfactory.com"
    SCRAPER_TIMEOUT_MS: int = 5000  # Default 5s (Playwright expects ms)

    # === MCP namespace ===
    NAMESPACE: str = "ffcal"

    # === MCP server transport ===
    MCP_TRANSPORT: str = "stdio"  # stdio | http | sse
    MCP_HOST: str = "127.0.0.1"  # only relevant for http/sse
    MCP_PORT: int = 8000  # only relevant for http/sse

    # === Default HTTP headers for Playwright ===
    USER_AGENT: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/127.0.0.0 Safari/537.36"
    )
    ACCEPT: str = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    ACCEPT_LANGUAGE: str = "en-US,en;q=0.9"

    # === Event field filtering ===
    INCLUDE_FIELDS: Optional[List[str]] = None
    EXCLUDE_FIELDS: Optional[List[str]] = None

    LOCAL_TIMEZONE: str = "UTC"

    # Tell Pydantic to look for environment variables in `.env`
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @field_validator("INCLUDE_FIELDS", "EXCLUDE_FIELDS", mode="before")
    @classmethod
    def split_comma_or_blank(cls, v):
        """
        Normalize values:
        - blank string → None
        - comma separated → list
        - JSON array → list
        """
        if v is None:
            return None
        if isinstance(v, str):
            v = v.strip()
            if not v:  # blank string
                return None
            return [x.strip() for x in v.split(",") if x.strip()]
        return v

    @property
    def default_fields(self) -> list[str]:
        """Default lean set of fields if INCLUDE_FIELDS not set."""
        return [
            "id",
            "title",
            "currency",
            "impact",
            "datetime",
            "forecast",
            "previous",
            "actual",
        ]

    @property
    def extra_http_headers(self) -> dict[str, str]:
        """
        Build the HTTP headers dict for Playwright requests.
        Returns values that can be directly passed to `page.set_extra_http_headers()`.
        """
        return {
            "User-Agent": self.USER_AGENT,
            "Accept": self.ACCEPT,
            "Accept-Language": self.ACCEPT_LANGUAGE,
        }

    @property
    def local_tz(self) -> ZoneInfo:
        try:
            return ZoneInfo(self.LOCAL_TIMEZONE)
        except Exception:
            # fallback to system local timezone
            try:
                return get_localzone()
            except Exception:
                return ZoneInfo("UTC")


@lru_cache
def get_settings() -> Settings:
    """
    Cached accessor for the global Settings instance.

    Using @lru_cache ensures:
      - Settings are instantiated only once per process.
      - No accidental recreation of config objects on every import.
      - Easy reset in tests (`get_settings.cache_clear()`).

    Returns:
        Settings: The singleton configuration instance.
    """
    return Settings()
