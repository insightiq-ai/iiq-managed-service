from datetime import datetime


def cast_iso_formatted_string_to_datetime(value: str) -> datetime:
    # Convert the iso-formatted datetime string to a datetime object
    return datetime.fromisoformat(value)
