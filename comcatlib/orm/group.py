"""Group membership of users."""

from __future__ import annotations
from typing import Union

from peewee import ForeignKeyField, IntegerField, ModelSelect

from cmslib.orm.group import Group
from mdb import Address, Company, Customer, Tenement

from comcatlib.orm.common import ComCatModel
from comcatlib.orm.user import User


__all__ = ['GroupMemberUser']


class GroupMemberUser(ComCatModel):  # pylint: disable=R0901
    """ComCat users as group members."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'group_member_user'

    group = ForeignKeyField(
        Group, column_name='group', on_delete='CASCADE', lazy_load=False)
    user = ForeignKeyField(
        User, column_name='user', on_delete='CASCADE', lazy_load=False)
    index = IntegerField(default=0)

    @classmethod
    def from_json(cls, json: dict, user: Union[User, int],
                  group: Union[Group, int], **kwargs) -> GroupMemberUser:
        """Creates a member for the given group
        from the respective JSON-ish dictionary.
        """
        record = super().from_json(json, **kwargs)
        record.user = user
        record.group = group
        return record

    @classmethod
    def select(cls, *args, cascade: bool = False, **kwargs) -> ModelSelect:
        """Selects group <> user mappings."""
        if not cascade:
            return super().select(*args, **kwargs)

        args = {cls, Group, User, Tenement, Customer, Company, Address, *args}
        return super().select(*args, **kwargs).join(Group).join_from(
            cls, User).join(Tenement).join(Customer).join(Company).join_from(
            Tenement, Address)

    def to_json(self) -> dict:
        """Returns a JSON-ish dict."""
        return {
            'id': self.id,
            'index': self.index,
            'group': self.group.id,
            'user': self.user.id
        }
