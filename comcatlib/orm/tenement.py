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

    @classmethod
    def from_json(cls, json, customer, **kwargs):
        """Returns a new tenement from a JSON-ish
        dict for the specified customer.
        """
        address = json.pop('address', None)
        address = Address.by_value(address, customer)
        address.save()
        tenement = super().from_json(json, **kwargs)
        tenement.customer = customer
        tenement.address = address
        return tenement

    def patch_json(self, json, **kwargs):
        """Patches the tenement with the data from a JSON-ish dict."""
        try:
            address = json.pop('address')
        except KeyError:
            address = self.address
        else:
            address = Address.by_value(address, self.customer)
            address.save()

        super().patch_json(json, **kwargs)
        self.address = address

    def to_json(self, cascade=False, **kwargs):
        """Returns JSON-ish dict."""
        dictionary = super().to_json(**kwargs)

        if cascade and self.address is not None:
            dictionary['address'] = self.address.to_json(**kwargs)

        return dictionary
