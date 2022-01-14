"""Exported functions."""

from typing import Union

from peewee import Select

from cmslib import Group

from comcatlib.orm.group import GroupMemberUser
from comcatlib.orm.user import User


__all__ = ['get_groups_of']


def get_groups_of(user: Union[User, int]) -> Select:
    """Select groups of the given user."""

    return Group.select(cascade=True).join_from(
        Group, GroupMemberUser,
        on=GroupMemberUser.group == Group.id
    ).where(GroupMemberUser.user == user)
