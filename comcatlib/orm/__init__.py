"""Object relational mappings."""


from comcatlib.orm.account import get_account, Account
from comcatlib.orm.address import Address
from comcatlib.orm.common import DATABASE, ComCatModel
from comcatlib.orm.content import AccountBaseChart
from comcatlib.orm.content import AccountConfiguration
from comcatlib.orm.content import AccountMenu
from comcatlib.orm.damage_report import AccountDamageReport
from comcatlib.orm.group import GroupMemberAccount
from comcatlib.orm.session import Session
from comcatlib.orm.tenement import Tenement


__all__ = [
    'DATABASE',
    'MODELS',
    'get_account',
    'Account',
    'Address',
    'AccountBaseChart',
    'AccountConfiguration',
    'AccountMenu',
    'AccountDamageReport',
    'ComCatModel',
    'GroupMemberAccount',
    'Session',
    'Tenement']


# Order matters here.
MODELS = (
    Address, Tenement, Account, Session, AccountBaseChart,
    AccountConfiguration, AccountMenu, AccountDamageReport, GroupMemberAccount)
