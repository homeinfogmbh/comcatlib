"""Tenant-to-tenant messaging."""

from peewee import ForeignKeyField

from tenant2tenant import TenantMessage

from comcatlib.orm.common import ComCatModel
from comcatlib.orm.user import User


__all__ = ['UserTenantMessage']


class UserTenantMessage(ComCatModel):   # pylint: disable=R0903
    """A user-issued tenant-to-tenant message."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'user_tenant_message'

    tenant_message = ForeignKeyField(
        TenantMessage, column_name='tenant_message', on_delete='CASCADE')
    issuer = ForeignKeyField(User, column_name='user', on_delete='CASCADE')

    def to_json(self, *args, **kwargs):
        """Returns a JSON-ish dict."""
        json = self.tenant_message.to_json(*args, **kwargs)
        json['issuer'] = self.issuer_id     # pylint: disable=E1101
        return json
