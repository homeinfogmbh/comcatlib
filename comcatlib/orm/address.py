"""ComCat addresses."""

from peewee import CharField, ForeignKeyField

from mdb import Customer

from comcatlib.orm.common import ComCatModel


__all__ = ['Address']


class Address(ComCatModel):
    """Addresses."""

    customer = ForeignKeyField(
        Customer, column_name='customer', on_delete='CASCADE')
    street = CharField(64)
    house_number = CharField(8)
    zip_code = CharField(32)
    city = CharField(64)

    @classmethod
    def for_customer(cls, ident, customer):
        """Returns the address for the respective customer."""
        return cls.get((cls.id == ident) & (cls.customer == customer))
