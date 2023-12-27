from typing import Optional


class TooManyRequestException(Exception):
    def __init__(self, message: Optional[str] = None):
        self.message = message
