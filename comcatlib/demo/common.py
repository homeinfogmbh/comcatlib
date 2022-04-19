"""Common constants and functions."""

from datetime import datetime, timedelta
from logging import getLogger
from pathlib import Path
from random import randint, shuffle
from typing import Iterator, Sequence, TypeVar


__all__ = [
    'DEMO_CUSTOMER_ID',
    'DEMO_DATASET_FILE',
    'DEMO_DATASET_ATTACHMENTS',
    'DEMO_USER_ADDRESS',
    'DEMO_USER_EMAIL',
    'DEMO_USER_NAME',
    'DEMO_USER_PASSWD',
    'LOG_FORMAT',
    'LOGGER',
    'get_random_date',
    'month_range',
    'randdate',
    'rand_date_in_month',
    'randzipfill'
]


DEMO_CUSTOMER_ID = 5000
DEMO_DATASET_FILE = Path('/usr/local/etc/comcat.d/demo.json')
DEMO_DATASET_ATTACHMENTS = Path('/usr/local/etc/comcat.d/demo.d')
DEMO_USER_ADDRESS = ('Schweidnitzer Weg', '6', '30159', 'Hannover')
DEMO_USER_EMAIL = 'mieterapp-demo@homeinfo.de'
DEMO_USER_NAME = 'Luca Musterberg'
DEMO_USER_PASSWD = 'mieterapp123'
LOG_FORMAT = '[%(levelname)s] %(name)s: %(message)s'
LOGGER = getLogger('demo-data-manager')

TargetType = TypeVar('TargetType')
ItemType = TypeVar('ItemType')


def get_random_date(days: int = 60) -> datetime:
    """Returns a random datetime within the given amount of days."""

    return randdate((now := datetime.now()) - timedelta(days=days), now)


def month_range() -> tuple[datetime, datetime]:
    """Returns a datetime range, covering the current month."""

    start = datetime.now().replace(
        day=1, hour=0, minute=0, second=0, microsecond=0
    )
    next_month = start + timedelta(days=31)
    last_day = next_month - timedelta(days=next_month.day)
    end = last_day.replace(hour=23, minute=59, second=59, microsecond=999999)
    return start, end


def randdate(start: datetime, end: datetime) -> datetime:
    """Creates a random datetime between start and end."""

    return datetime.fromtimestamp(randint(
        round(start.timestamp()), round(end.timestamp())
    ))


def rand_date_in_month() -> datetime:
    """Returns a random datetime within the current month."""

    return randdate(*month_range())


def randzipfill(
        targets: Sequence[TargetType],
        items: Sequence[ItemType]
) -> Iterator[tuple[TargetType, ItemType]]:
    """Yields tuples of randomized targets combined with the given items."""

    extended_targets = list(targets)

    while len(extended_targets) < len(items):
        extended_targets.extend(targets)

    shuffle(extended_targets)
    return zip(extended_targets, items)
