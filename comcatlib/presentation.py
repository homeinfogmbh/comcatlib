"""Presentations for ComCat accounts."""

from cmslib.dom import presentation
from cmslib.exceptions import NoConfigurationFound
from cmslib.orm.charts import BaseChart
from cmslib.orm.configuration import Configuration
from cmslib.orm.menu import Menu
from cmslib.presentation.common import PresentationMixin

from comcatlib.orm import GroupMemberUser
from comcatlib.orm import User
from comcatlib.orm import UserBaseChart
from comcatlib.orm import UserConfiguration
from comcatlib.orm import UserMenu


__all__ = ['Presentation']


class Presentation(PresentationMixin):
    """Accumulates content for a ComCat user."""

    def __init__(self, user: User):
        """Sets the respective user."""
        self.user = user
        self.cache = {}

    @property
    def customer(self):
        """Returns the respective customer."""
        return self.user.customer

    @property
    def base_charts(self):
        """Yields the user's base charts."""
        return UserBaseChart.select().join(BaseChart).where(
            (UserBaseChart.user == self.user)
            & (BaseChart.trashed == 0)).order_by(UserBaseChart.index)

    @property
    def configuration(self):
        """Returns the user's configuration."""
        try:
            return Configuration.select().join(UserConfiguration).where(
                UserConfiguration.user == self.user).get()
        except Configuration.DoesNotExist:
            raise NoConfigurationFound() from None

    @property
    def groups(self):
        """Yields groups this user is a member of."""
        for gma in GroupMemberUser.select().where(
                GroupMemberUser.user == self.user):
            yield gma.group

    @property
    def menus(self):
        """Yields menus of this user."""
        return Menu.select().join(UserMenu).where(UserMenu.user == self.user)

    def to_dom(self) -> presentation.typeDefinition():
        """Returns an XML DOM."""
        xml = super().to_dom()
        xml.user = self.user.uuid.hex
        return xml

    def to_json(self) -> dict:
        """Returns a JSON-ish dict."""
        json = super().to_json()
        json['user'] = self.user.uuid.hex
        return json
