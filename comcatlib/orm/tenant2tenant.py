"""Tenant-to-tenant messaging."""

from peewee import ForeignKeyField, ModelSelect

from mdb import Address, Company, Customer, Tenement
from tenant2tenant import TenantMessage

from comcatlib.orm.common import ComCatModel
from comcatlib.orm.user import User


__all__ = ['UserTenantMessage']


class UserTenantMessage(ComCatModel):   # pylint: disable=R0903
    """A user-issued tenant-to-tenant message."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'user_tenant_message'

    tenant_message = ForeignKeyField(
        TenantMessage, column_name='tenant_message', on_delete='CASCADE',
        lazy_load=False)
    user = ForeignKeyField(
        User, column_name='user', on_delete='CASCADE', lazy_load=False)

    @classmethod
    def select(cls, *args, cascade: bool = False, **kwargs) -> ModelSelect:
        """Selects clients."""
        if not cascade:
            return super().select(*args, **kwargs)

        args = {
            cls, TenantMessage, User, Tenement, Customer, Company, Address,
            *args
        }
        return super().select(*args, **kwargs).join(TenantMessage).join_from(
            cls, User).join(Tenement).join(Customer).join(Company).join_from(
            Tenement, Address)
