"""Group membership of accounts."""

from peewee import ForeignKeyField, IntegerField

from cmslib.orm.group import Group
from his.messages.data import MISSING_KEY_ERROR, INVALID_KEYS

from comcatlib.orm.account import get_account, Account
from comcatlib.orm.common import ComCatModel


__all__ = ['GroupMemberAccount']


class GroupMemberAccount(ComCatModel):  # pylint: disable=R0901
    """ComCat accounts as group members."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'group_member_account'

    group = ForeignKeyField(Group, column_name='group', on_delete='CASCADE')
    account = ForeignKeyField(
        Account, column_name='account', on_delete='CASCADE')
    index = IntegerField(default=0)

    @classmethod
    def from_json(cls, json, group):
        """Creates a member for the given group
        from the respective JSON-ish dictionary.
        """
        try:
            account = json.pop('account')
        except KeyError:
            raise MISSING_KEY_ERROR.update(keys=['account'])

        account = get_account(account)
        index = json.pop('index', 0)

        if json:
            raise INVALID_KEYS.update(keys=tuple(json))

        return cls(group=group, account=account, index=index)

    def to_json(self):
        """Returns a JSON-ish dict."""
        return {
            'id': self.id,
            'index': self.index,
            'group': self.group.id,
            'account': self.account.id}
