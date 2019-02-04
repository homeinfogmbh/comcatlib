"""Group membership of accounts."""

from peewee import ForeignKeyField

from cmslib.orm.group import group_fk, GroupMember

from comcatlib.orm.auth import Account
from comcatlib.orm.common import ComCatModel


__all__ = ['GroupMemberAccount']


class GroupMemberAccount(ComCatModel, GroupMember):  # pylint: disable=R0901
    """ComCat accounts as group members."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'group_member_account'

    group = group_fk('accounts')
    member = ForeignKeyField(
        Account, column_name='account', on_delete='CASCADE')

    def to_dom(self):
        """Returns an XML DOM."""
        raise NotImplementedError()

    def to_json(self):
        """Returns a JSON-ish dict."""
        return {
            'member': self.id,
            'account': self.member.id,
            'index': self.index}
