"""ComCat addresses."""

from peewee import CharField

from comcatlib.orm.common import ComCatModel


__all__ = ['Address']


class Address(ComCatModel):
    """Addresses."""

    street = CharField(64)
    house_number = CharField(8)
    zip_code = CharField(32)
    city = CharField(64)
