"""ComCat addresses."""

from contextlib import suppress

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

    @classmethod
    def from_json(cls, json, customer, unique=True, **kwargs):
        """Adds a new address from JSON."""
        address = super().from_json(json, **kwargs)

        if unique:
            with suppress(cls.DoesNotExist):
                return cls.get(
                    (cls.customer == customer)
                    & (cls.street == address.street)
                    & (cls.house_number == address.house_number)
                    & (cls.zip_code == address.zip_code)
                    & (cls.city == address.city))

        address.customer = customer
        return address

    @classmethod
    def patch_json(cls, *_, **__):
        """Prohibit patching."""
        raise NotImplementedError('Patching not implemented.')
