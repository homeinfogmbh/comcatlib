"""Tenement management."""

from typing import Union

from peewee import IntegrityError

from mdb import Address, Customer, Tenement

from comcatlib.demo.common import LOGGER


__all__ = ['create_tenement', 'delete_tenements']


def create_tenement(
        customer: Union[Customer, int],
        street: str,
        house_number: str,
        zip_code: str,
        city: str
) -> Tenement:
    """Creates a new tenement."""

    address = Address.add(street, house_number, zip_code, city)
    address.save()
    tenement = Tenement(customer=customer, address=address)
    tenement.save()
    return tenement


def delete_tenements(customer: Union[Customer, int]) -> None:
    """Deletes all tenements of the given customer."""

    for tenement in Tenement.select().join(Address).where(
            Tenement.customer == customer
    ):
        try:
            tenement.delete_instance()
        except IntegrityError:
            LOGGER.warning('Cannot delete tenement: %s', tenement.address)
        else:
            LOGGER.info('Deleted tenement: %s', tenement.address)
