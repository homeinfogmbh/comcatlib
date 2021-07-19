"""User registration."""

from __future__ import annotations
from datetime import datetime
from typing import Union

from peewee import CharField, DateTimeField, ForeignKeyField, ModelSelect

from mdb import Customer, Tenement

from comcatlib.exceptions import AlreadyRegistered, DuplicateUser
from comcatlib.functions import genpw
from comcatlib.orm.common import ComCatModel
from comcatlib.orm.user import User


__all__ = ['UserRegistration']


class UserRegistration(ComCatModel):    # pylint: disable=R0903
    """A user registration."""

    class Meta:     # pylint: disable=R0903,C0115
        table_name = 'user_registration'

    name = CharField()
    email = CharField()
    tenant_id = CharField()
    customer = ForeignKeyField(
        Customer, column_name='customer', on_delete='CASCADE')
    registered = DateTimeField(default=datetime.now)

    @classmethod
    def same_ids_sel(cls, tenant_id: str, email: str) -> ModelSelect:
        """Returns a select condition to match records with the same IDs."""
        return (cls.tenant_id == tenant_id) | (cls.email == email)

    @classmethod
    def dupes_select(cls, tenant_id: str, email: str,
                     customer: Union[Customer, int]) -> ModelSelect:
        """Returns a select condition to match duplicales."""
        return cls.same_ids_sel(tenant_id, email) & (cls.customer == customer)

    @classmethod
    def add(cls, name: str, email: str, tenant_id: str,
            customer: Union[Customer, int]) -> UserRegistration:
        """Adds a new user registration."""
        condition = cls.dupes_select(tenant_id, email, customer)

        try:
            record = cls.select().where(condition).get()
        except cls.DoesNotExist:
            return cls(name=name, email=email, tenant_id=tenant_id,
                       customer=customer)

        raise AlreadyRegistered(record)

    def confirm(self, tenement: Tenement):
        """Confirm the user registration."""
        passwd = genpw()
        user = User(tenement=tenement, passwd=passwd)
        self.delete_instance()

        if user.is_unique:
            return (user, passwd)

        raise DuplicateUser()
