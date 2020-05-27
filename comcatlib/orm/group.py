"""Group membership of users."""

from peewee import ForeignKeyField, IntegerField

from cmslib.orm.group import Group
from his.messages.data import MISSING_KEY_ERROR, INVALID_KEYS

from comcatlib.orm.common import ComCatModel
from comcatlib.orm.user import get_user, User


__all__ = ['GroupMemberUser']


class GroupMemberUser(ComCatModel):  # pylint: disable=R0901
    """ComCat users as group members."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'group_member_user'

    group = ForeignKeyField(Group, column_name='group', on_delete='CASCADE')
    user = ForeignKeyField(User, column_name='user', on_delete='CASCADE')
    index = IntegerField(default=0)

    @classmethod
    def from_json(cls, json, group):
        """Creates a member for the given group
        from the respective JSON-ish dictionary.
        """
        try:
            user = json.pop('user')
        except KeyError:
            raise MISSING_KEY_ERROR.update(keys=['user'])

        user = get_user(user)
        index = json.pop('index', 0)

        if json:
            raise INVALID_KEYS.update(keys=tuple(json))

        return cls(group=group, user=user, index=index)

    def to_json(self):
        """Returns a JSON-ish dict."""
        return {
            'id': self.id,
            'index': self.index,
            'group': self.group.id,
            'user': self.user.id
        }
