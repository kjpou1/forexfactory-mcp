from datetime import datetime
from enum import Enum


class TimePeriod(Enum):
    TOMORROW = "tomorrow"
    NEXT_WEEK = "next_week"
    NEXT_MONTH = "next_month"
    TODAY = "today"
    THIS_WEEK = "this_week"
    THIS_MONTH = "this_month"
    YESTERDAY = "yesterday"
    LAST_WEEK = "last_week"
    LAST_MONTH = "last_month"
    CUSTOM = "custom"  # New addition for custom date range

    @staticmethod
    def from_text(text):
        if text is None:
            raise ValueError("Input text cannot be None")
        text = text.strip().lower().replace(" ", "_")
        mapping = {
            "tomorrow": TimePeriod.TOMORROW,
            "next_week": TimePeriod.NEXT_WEEK,
            "next_month": TimePeriod.NEXT_MONTH,
            "today": TimePeriod.TODAY,
            "this_week": TimePeriod.THIS_WEEK,
            "this_month": TimePeriod.THIS_MONTH,
            "yesterday": TimePeriod.YESTERDAY,
            "last_week": TimePeriod.LAST_WEEK,
            "last_month": TimePeriod.LAST_MONTH,
            "custom": TimePeriod.CUSTOM,
        }
        if text not in mapping:
            raise ValueError(f"Invalid text for TimePeriod: '{text}'")
        return mapping[text]

    @staticmethod
    def to_file_name_ending(enum_value):
        reverse_mapping = {
            TimePeriod.TOMORROW: "tomorrow",
            TimePeriod.NEXT_WEEK: "next_week",
            TimePeriod.NEXT_MONTH: "next_month",
            TimePeriod.TODAY: "today",
            TimePeriod.THIS_WEEK: "this_week",
            TimePeriod.THIS_MONTH: "this_month",
            TimePeriod.YESTERDAY: "yesterday",
            TimePeriod.LAST_WEEK: "last_week",
            TimePeriod.LAST_MONTH: "last_month",
            TimePeriod.CUSTOM: "custom",  # New addition for custom date range
        }
        if enum_value not in reverse_mapping:
            raise ValueError(f"Invalid TimePeriod value: '{enum_value}'")
        return reverse_mapping[enum_value]

    @staticmethod
    def to_text(enum_value):
        reverse_mapping = {
            TimePeriod.TOMORROW: "Tomorrow",
            TimePeriod.NEXT_WEEK: "Next Week",
            TimePeriod.NEXT_MONTH: "Next Month",
            TimePeriod.TODAY: "Today",
            TimePeriod.THIS_WEEK: "This Week",
            TimePeriod.THIS_MONTH: "This Month",
            TimePeriod.YESTERDAY: "Yesterday",
            TimePeriod.LAST_WEEK: "Last Week",
            TimePeriod.LAST_MONTH: "Last Month",
            TimePeriod.CUSTOM: "Custom",  # New addition for custom date range
        }
        if enum_value not in reverse_mapping:
            raise ValueError(f"Invalid TimePeriod value: '{enum_value}'")
        return reverse_mapping[enum_value]

    @staticmethod
    def to_href(value):
        if isinstance(value, str):
            value = TimePeriod.from_text(value)
        if not isinstance(value, TimePeriod):
            raise ValueError(f"Invalid TimePeriod value: '{value}'")

        href_mapping = {
            TimePeriod.TOMORROW: "/calendar?day=tomorrow",
            TimePeriod.NEXT_WEEK: "/calendar?week=next",
            TimePeriod.NEXT_MONTH: "/calendar?month=next",
            TimePeriod.TODAY: "/calendar?day=today",
            TimePeriod.THIS_WEEK: "/calendar?week=this",
            TimePeriod.THIS_MONTH: "/calendar?month=this",
            TimePeriod.YESTERDAY: "/calendar?day=yesterday",
            TimePeriod.LAST_WEEK: "/calendar?week=last",
            TimePeriod.LAST_MONTH: "/calendar?month=last",
            TimePeriod.CUSTOM: "/calendar?range=",
        }
        return href_mapping[value]

    @staticmethod
    def validate_date_format(date_text):
        try:
            datetime.strptime(date_text, "%Y-%m-%d")
        except ValueError:
            raise ValueError(
                f"Incorrect date format, should be YYYY-MM-DD: '{date_text}'"
            )
        return date_text


# # Example usage
# try:
#     print(TimePeriod.from_text('Tomorrow'))       # Output: TimePeriod.TOMORROW
#     print(TimePeriod.to_text(TimePeriod.TOMORROW))  # Output: 'Tomorrow'
#     print(TimePeriod.to_href('Tomorrow'))          # Output: '/calendar?day=tomorrow'
#     print(TimePeriod.to_href(TimePeriod.NEXT_WEEK)) # Output: '/calendar?week=next'
# except ValueError as e:
#     print(e)
