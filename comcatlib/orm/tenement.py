"""Tenements."""

from peewee import CharField
from peewee import ForeignKeyField

from mdb import Address, Customer

from comcatlib.messages import INVALID_TENEMENT, NO_SUCH_TENEMENT
from comcatlib.orm.common import ComCatModel


__all__ = ['Tenement']


class Tenement(ComCatModel):
    """A tenement."""

    customer = ForeignKeyField(Customer, column_name='customer')
    address = ForeignKeyField(Address, column_name='address', null=True)
    rental_unit = CharField(255, null=True)     # Mieteinheit / ME.
    living_unit = CharField(255, null=True)     # Wohneinheit / WE.
    name = CharField(255, null=True)    # Name of the tenant.
    annotation = CharField(255, null=True)

    @classmethod
    def from_json(cls, json, customer, **kwargs):
        """Returns a new tenement from a JSON-ish
        dict for the specified customer.
        """
        address = json.pop('address', None)
        tenement = super().from_json(json, **kwargs)
        tenement.customer = customer
        tenement.address = Address.by_value(address, customer)
        return tenement

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
                raise NO_SUCH_TENEMENT

        if isinstance(value, dict):
            tenement = cls.from_json(value, customer)
            tenement.save()
            return tenement

        raise INVALID_TENEMENT

    def save(self, *args, **kwargs):
        """Saves the record."""
        if self.address is not None:
            self.address.save(*args, **kwargs)

        return super().save(*args, **kwargs)

    def patch_json(self, json, **kwargs):
        """Patches the tenement with the data from a JSON-ish dict."""
        try:
            address = json.pop('address')
        except KeyError:
            address = self.address
        else:
            address = Address.by_value(address, self.customer)

        super().patch_json(json, **kwargs)
        self.address = address

    def to_json(self, cascade=False, **kwargs):
        """Returns JSON-ish dict."""
        dictionary = super().to_json(**kwargs)

        if cascade and self.address is not None:
            dictionary['address'] = self.address.to_json(**kwargs)

        return dictionary
