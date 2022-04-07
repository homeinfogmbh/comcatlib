"""Common constants and functions."""

from datetime import datetime
from random import randint


__all__ = ['DEMO_CUSTOMER_ID', 'randdate']


DEMO_CUSTOMER_ID = 5000


def randdate(start: datetime, end: datetime) -> datetime:
    """Creates a random datetime for the record."""

    return datetime.fromtimestamp(randint(
        round(start.timestamp()), round(end.timestamp())
    ))
