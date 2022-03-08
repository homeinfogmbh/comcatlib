"""Exported functions."""

from typing import Iterator, Optional, Union

from cmslib import Group, Groups

from comcatlib.orm.group import GroupMemberUser
from comcatlib.orm.user import User


__all__ = ['get_group_ids', 'get_groups_lineage']


def get_group_ids(user: Union[User, int]) -> Iterator[int]:
    """Yield group IDs of the given user."""

    for group_member_user in GroupMemberUser.select().where(
            GroupMemberUser.user == user
    ):
        yield group_member_user.group


def get_groups_lineage(
        user: Union[User, int], *,
        groups: Optional[Groups] = None
) -> Iterator[Group]:
    """Select the groups-lineage of the given user."""

    if groups is None:
        groups = Groups.for_customer(user.tenement.customer)

    for member_group in groups.groups(get_group_ids(user)):
        for group in groups.lineage(member_group):
            yield group
