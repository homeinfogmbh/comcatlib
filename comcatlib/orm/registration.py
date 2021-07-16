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

    name = CharField()
    email = CharField()
    tenant_id = CharField()
    customer = ForeignKeyField(
        Customer, column_name='customer', on_delete='CASCADE')
    registered = DateTimeField(default=datetime.now)

    @classmethod
    def add(cls, name: str, email: str, tenant_id: str,
            customer: Union[Customer, int]) -> UserRegistration:
        """Adds a new user registration."""
        try:
            record = cls.select().where(
                (
                    (cls.tenant_id == tenant_id)
                    | (cls.email == email)
                ) & (cls.customer == customer)
            ).get()
        except cls.DoesNotExist:
            return cls(name=name, email=email, tenant_id=tenant_id,
                       customer=customer)

        raise AlreadyRegistered(record)
