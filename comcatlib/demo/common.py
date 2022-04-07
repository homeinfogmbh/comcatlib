"""Common constants and functions."""

from datetime import datetime
from pathlib import Path
from random import randint, shuffle
from typing import Iterator, Sequence, TypeVar


__all__ = [
    'DEMO_CUSTOMER_ID',
    'DEMO_DATASET_FILE',
    'DEMO_DATASET_ATTACHMENTS',
    'randdate',
    'randzipfill'
]


DEMO_CUSTOMER_ID = 5000
DEMO_DATASET_FILE = Path('/usr/local/etc/comcat.d/demo.json')
DEMO_DATASET_ATTACHMENTS = Path('/usr/local/etc/comcat.d/demo.d')

TargetType = TypeVar('TargetType')
ItemType = TypeVar('ItemType')


def randdate(start: datetime, end: datetime) -> datetime:
    """Creates a random datetime for the record."""

    return datetime.fromtimestamp(randint(
        round(start.timestamp()), round(end.timestamp())
    ))


def randzipfill(
        targets: Sequence[TargetType],
        items: Sequence[ItemType]
) -> Iterator[tuple[TargetType, ItemType]]:
    """Yields tuples of randomized target combined with the given items."""

    extended_targets = list(targets)

    while len(extended_targets) < len(items):
        extended_targets.extend(targets)

    shuffle(extended_targets)
    return zip(extended_targets, items)
