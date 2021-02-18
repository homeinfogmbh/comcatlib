"""Customer-specific settings."""

from __future__ import annotations
from typing import Union

from peewee import JOIN, ForeignKeyField, IntegerField, ModelSelect

from mdb import Address, Company, Customer, Tenement

from comcatlib.orm.common import ComCatModel
from comcatlib.orm.user import User


__all__ = ['Settings']


USER_QUOTA = 10


class Settings(ComCatModel):
    """Customer-specific settings model."""

    customer = ForeignKeyField(
        Customer, column_name='customer', on_delete='CASCADE',
        on_update='DELETE')
    user_quota = IntegerField(default=USER_QUOTA)

    @classmethod
    def for_customer(cls, customer: Union[Customer, int]) -> Settings:
        """Returns the settings for the specified customer
        or creates a record if none exists yet.
        """
        try:
            return cls.select(cascade=True).where(
                cls.customer == customer).get()
        except cls.DoesNotExist:
            record = cls(customer=customer)
            record.save()
            return record

    @classmethod
    def select(cls, *args, cascade: bool = False, **kwargs) -> ModelSelect:
        """"Selects Settings."""
        if not cascade:
            return super().select(*args, **kwargs)

        args = {cls, Customer, Company, Address, *args}
        return cls.select(*args, **kwargs).join(Customer).join(Company).join(
            Address, join_type=JOIN.LEFT_OUTER)

    def allocate_user(self) -> bool:
        """Allocates a user account."""
        users = User.select(cascade=True).where(
            Tenement.customer == self.customer)
        return len(users) < self.user_quota
