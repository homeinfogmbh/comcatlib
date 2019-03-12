"""ComCat addresses."""

from peewee import CharField, ForeignKeyField

from mdb import Customer

from comcatlib.orm.common import ComCatModel


__all__ = ['Address']


class Address(ComCatModel):
    """Addresses."""

    customer = ForeignKeyField(Customer, column_name='customer')
    street = CharField(64)
    house_number = CharField(8)
    zip_code = CharField(32)
    city = CharField(64)
