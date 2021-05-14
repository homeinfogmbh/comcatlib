"""Presentations for ComCat accounts."""

from typing import Iterable

from cmslib import NoConfigurationFound
from cmslib import Configuration
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
        return user.tenement.customer

    @property
    def base_charts(self) -> Iterable[UserBaseChart]:
        """Yields the user's base charts."""
        return UserBaseChart.select(cascade=True).where(
            (UserBaseChart.user == self.user) & get_trashed()
        ).order_by(UserBaseChart.index)

    @property
    def configuration(self) -> Configuration:
        """Returns the user's configuration."""
        try:
            return Configuration.select(cascade=True).where(
                UserConfiguration.user == self.user).get()
        except Configuration.DoesNotExist:
            raise NoConfigurationFound() from None

    @property
    def groups(self) -> GroupMemberUser:
        """Yields groups this user is a member of."""
        for gma in GroupMemberUser.select(cascade=True).where(
                GroupMemberUser.user == self.user):
            yield gma.group

    @property
    def menus(self) -> Menu:
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
