"""Tenement management."""

from typing import Union

from mdb import Address, Customer, Tenement


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


def delete_tenements(customer: Union[Customer, int]) -> int:
    """Deletes all tenements of the given customer."""

    return Tenement.delete().where(Tenement.customer == customer).execute()
