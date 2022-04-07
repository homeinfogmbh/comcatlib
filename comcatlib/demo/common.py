"""Common constants and functions."""

from datetime import datetime
from pathlib import Path
from random import randint


__all__ = [
    'DEMO_CUSTOMER_ID',
    'DEMO_DATASET_FILE',
    'DEMO_DATASET_ATTACHMENTS',
    'randdate'
]


DEMO_CUSTOMER_ID = 5000
DEMO_DATASET_FILE = Path('/usr/local/etc/comcat.d/demo.json')
DEMO_DATASET_ATTACHMENTS = Path('/usr/local/etc/comcat.d/demo.d')


def randdate(start: datetime, end: datetime) -> datetime:
    """Creates a random datetime for the record."""

    return datetime.fromtimestamp(randint(
        round(start.timestamp()), round(end.timestamp())
    ))
