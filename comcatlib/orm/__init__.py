"""Object relational mappings."""

from comcatlib.orm.auth import Account, Session
from comcatlib.orm.address import Address
from comcatlib.orm.common import DATABASE, ComCatModel
from comcatlib.orm.content import AccountBaseChart
from comcatlib.orm.content import AccountConfiguration
from comcatlib.orm.content import AccountMenu
from comcatlib.orm.damage_report import AccountDamageReport
from comcatlib.orm.group import GroupMemberAccount


__all__ = [
    'DATABASE',
    'MODELS',
    'ComCatModel',
    'Account',
    'Address',
    'Session',
    'AccountBaseChart',
    'AccountConfiguration',
    'AccountMenu',
    'AccountDamageReport',
    'GroupMemberAccount']


# Order matters here.
MODELS = (
    Address, Account, Session, AccountBaseChart, AccountConfiguration,
    AccountMenu, AccountDamageReport, GroupMemberAccount)
