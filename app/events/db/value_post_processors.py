from datetime import datetime, date
from typing import Optional


def cast_iso_formatted_string_to_datetime(value: Optional[str]) -> Optional[datetime]:
    # Convert the iso-formatted datetime string to a datetime object
    if value:
        return datetime.fromisoformat(value)
    else:
        return None


def cast_iso_formatted_string_to_date(value: Optional[str]) -> Optional[date]:
    # Convert the iso-formatted datetime string to a date object
    if value:
        return datetime.fromisoformat(value).date()
    else:
        return None


def cast_string_to_int(value: Optional[str]) -> Optional[int]:
    # Convert the string to int
    if value:
        return int(value)
    else:
        return None


def cast_string_to_float(value: Optional[str]) -> Optional[float]:
    # Convert the string to integer
    if value:
        return float(value)
    else:
        return None


def cast_string_to_bool(value: Optional[str]) -> Optional[bool]:
    # Convert the string to bool
    if value is not None:
        return value.lower() == "true"
    else:
        return None
