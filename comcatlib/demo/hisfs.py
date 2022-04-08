"""HISFS integration."""

from hisfs import FileExists, File
from mdb import Customer

from comcatlib.demo.common import DEMO_CUSTOMER_ID, LOGGER


__all__ = ['get_or_create_file', 'remove_files']


def get_or_create_file(
        name: str,
        bytes_: bytes,
        *,
        customer: int = DEMO_CUSTOMER_ID
) -> File:
    """Creates or re-uses the given file."""

    LOGGER.info('Adding file: %s', name)

    try:
        file = File.add(name, customer, bytes_)
    except FileExists:
        return File.get((File.name == name) & (File.customer == customer))

    file.file.save()
    file.save()
    return file


def remove_files(customer: Customer) -> None:
    """Remove images of the given customer."""

    for file in File.select().where(File.customer == customer):
        file.delete_instance()
