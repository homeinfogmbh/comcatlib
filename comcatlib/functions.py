"""Common functions."""

from mdb import Tenement


__all__ = ['get_tenement']


def get_tenement(ident, customer):
    """Returns a tenement by its ID and customer."""

    condition = Tenement.id == ident
    condition &= Tenement.customer == customer
    return Tenement.get(condition)
