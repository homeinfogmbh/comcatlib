"""ComCat addresses."""

from contextlib import suppress

from peewee import CharField, ForeignKeyField

from mdb import Customer

from comcatlib.messages import INVALID_ADDRESS, NO_SUCH_ADDRESS
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

    def patch_json(self, **_):
        """Prohibit patching."""
        raise NotImplementedError('Patching not implemented.')

    @classmethod
    def by_value(cls, value, customer):
        """Returns an address by either ID or
        JSON-dict for the respective customer.
        """
        if value is None:
            return None

        if isinstance(value, int):
            try:
                return cls.get((cls.id == value) & (cls.customer == customer))
            except cls.DoesNotExist:
                raise NO_SUCH_ADDRESS

        if isinstance(value, dict):
            address = cls.from_json(value, customer)
            address.save()
            return address

        raise INVALID_ADDRESS
