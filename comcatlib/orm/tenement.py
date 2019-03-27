"""Tenements."""

from peewee import CharField
from peewee import ForeignKeyField

from mdb import Customer

from comcatlib.orm.address import Address
from comcatlib.orm.common import ComCatModel


__all__ = ['Tenement']


class Tenement(ComCatModel):
    """A ComCat account."""

    customer = ForeignKeyField(Customer, column_name='customer')
    address = ForeignKeyField(Address, column_name='address', null=True)
    rental_unit = CharField(255, null=True)     # Mieteinheit / ME.
    living_unit = CharField(255, null=True)     # Wohneinheit / WE.
    name = CharField(255, null=True)    # Name of the tenant.
    annotation = CharField(255, null=True)
