"""Presentations for ComCat accounts."""

from cmslib.exceptions import NoConfigurationFound
from cmslib.orm.charts import BaseChart
from cmslib.orm.configuration import Configuration
from cmslib.orm.group import GroupMemberAccount
from cmslib.orm.menu import Menu
from cmslib.presentation.common import PresentationMixin

from comcatlib.orm import AccountBaseChart, AccountConfiguration, AccountMenu


__all__ = ['Presentation']


class Presentation(PresentationMixin):
    """Accumulates content for a ComCat account."""

    def __init__(self, account):
        """Sets the respective account."""
        self.account = account
        self.cache = {}

    @property
    def customer(self):
        """Returns the respective customer."""
        return self.account.customer

    @property
    def base_charts(self):
        """Yields the account's base charts."""
        return AccountBaseChart.select().join(BaseChart).where(
            (AccountBaseChart.account == self.account)
            & (BaseChart.trashed == 0)).order_by(AccountBaseChart.index)

    @property
    def configuration(self):
        """Returns the account's configuration."""
        try:
            return Configuration.select().join(AccountConfiguration).where(
                AccountConfiguration.account == self.account).get()
        except Configuration.DoesNotExist:
            raise NoConfigurationFound()

    @property
    def groups(self):
        """Yields groups this account is a member of."""
        for gma in GroupMemberAccount.select().where(
                GroupMemberAccount.account == self.account):
            yield gma.group

    @property
    def menus(self):
        """Yields menus of this account."""
        return Menu.select().join(AccountMenu).where(
            AccountMenu.account == self.account)

    def to_dom(self):
        """Returns an XML DOM."""
        xml = super().to_dom()
        xml.account = self.account.uuid.hex
        return xml

    def to_json(self):
        """Returns a JSON-ish dict."""
        json = super().to_json()
        json['account'] = self.account.uuid.hex
        return json
