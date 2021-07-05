"""User registration."""

from __future__ import annotations
from datetime import datetime
from typing import Union

from peewee import CharField, DateTimeField, ForeignKeyField

from mdb import Customer

from comcatlib.exceptions import AlreadyRegistered
from comcatlib.orm.common import ComCatModel


__all__ = ['UserRegistration']


class UserRegistration(ComCatModel):
    """A user registration."""

    first_name = CharField()
    last_name = CharField()
    tenant_id = CharField()
    customer = ForeignKeyField(
        Customer, column_name='customer', on_delete='CASCADE')
    registered = DateTimeField(default=datetime.now)

    @classmethod
    def add(cls, first_name: str, last_name: str, tenant_id: str,
            customer: Union[Customer, int]) -> UserRegistration:
        """Adds a new user registration."""
        try:
            record = cls.select().where(
                (cls.tenant_id == tenant_id) & (cls.customer == customer)
            ).get()
        except cls.DoesNotExist:
            return cls(first_name=first_name, last_name=last_name,
                       tenant_id=tenant_id, customer=customer)

        raise AlreadyRegistered(record)
