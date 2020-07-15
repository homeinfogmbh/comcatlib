"""Tenant-to-tenant messaging."""

from peewee import ForeignKeyField

from tenant2tenant import TenantMessage

from comcalib.orm.common import ComCatModel
from comcalib.orm.user import User


__all__ = ['UserTenantMessage']


class UserTenantMessage(ComCatModel):
    """A user-issued tenant-to-tenant message."""

    tenant_message = ForeignKeyField(
        TenantMessage, column_name='tenant_message', on_delete='CASCADE')
    issuer = ForeignKeyField(User, column_name='user', on_delete='CASCADE')
