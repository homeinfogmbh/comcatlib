"""Presentations for ComCat accounts."""

from typing import Iterator

from cmslib import BaseChart
from cmslib import Configuration
from cmslib import Group
from cmslib import Menu
from cmslib import Presentation
from cmslib import get_trashed
from cmslib.dom import presentation

from comcatlib.orm import GroupMemberUser
from comcatlib.orm import User
from comcatlib.orm import UserBaseChart
from comcatlib.orm import UserConfiguration
from comcatlib.orm import UserMenu


__all__ = ['Presentation']


PresentationDOM = presentation.typeDefinition()


class Presentation(Presentation):   # pylint: disable=E0102
    """Accumulates content for a ComCat user."""

    def __init__(self, user: User):     # pylint: disable=W0231
        """Sets the respective user."""
        self.user = user

    @property
    def customer(self):
        """Returns the customer."""
        return self.user.tenement.customer

    def get_base_charts(self) -> Iterator[BaseChart]:
        """Yields the user's base charts."""
        for user_base_chart in UserBaseChart.select(cascade=True).where(
                (UserBaseChart.user == self.user) & get_trashed()).order_by(
                UserBaseChart.index):
            yield (user_base_chart.index, user_base_chart.base_chart)

    def get_configurations(self) -> Iterator[Configuration]:
        """Returns the user's configuration."""
        for user_configuration in UserConfiguration.select(cascade=True).where(
                UserConfiguration.user == self.user):
            yield user_configuration.configuration

    def get_memberships(self) -> Iterator[Group]:
        """Yields groups this user is a member of."""
        for gma in GroupMemberUser.select(cascade=True).where(
                GroupMemberUser.user == self.user):
            yield gma.group

    def get_menus(self) -> Iterator[Menu]:
        """Yields menus of this user."""
        return Menu.select(cascade=True).join_from(Menu, UserMenu).where(
            UserMenu.user == self.user)

    def to_dom(self) -> PresentationDOM:
        """Returns an XML DOM."""
        xml = super().to_dom()
        xml.user = self.user.id
        return xml

    def to_json(self) -> dict:
        """Returns a JSON-ish dict."""
        json = super().to_json()
        json['user'] = self.user.id
        return json
