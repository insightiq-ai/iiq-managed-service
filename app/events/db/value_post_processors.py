import json
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


def cast_to_json(value: Optional) -> Optional[str]:
    # Convert any to json-string
    if value is not None:
        return json.dumps(value)
    else:
        return None


def cast_integer_to_string(value: Optional[int]) -> Optional[str]:
    # Convert the integer to string
    if value:
        return str(value)
    else:
        return None


def cast_python_list_to_postgres_list(value: Optional[list]) -> Optional[str]:
    if value:
        return '{' + ','.join(value) + '}'
    else:
        return None
