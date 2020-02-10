"""Object relational mappings."""


from comcatlib.orm.address import Address
from comcatlib.orm.common import DATABASE, ComCatModel
from comcatlib.orm.content import UserBaseChart
from comcatlib.orm.content import UserConfiguration
from comcatlib.orm.content import UserMenu
from comcatlib.orm.damage_report import UserDamageReport
from comcatlib.orm.group import GroupMemberUser
from comcatlib.orm.oauth import AuthorizationCode
from comcatlib.orm.oauth import Client
from comcatlib.orm.oauth import Token
from comcatlib.orm.session import Session
from comcatlib.orm.tenement import Tenement
from comcatlib.orm.user import User


__all__ = [
    'DATABASE',
    'MODELS',
    'create_tables',
    'User',
    'Address',
    'UserBaseChart',
    'UserConfiguration',
    'UserMenu',
    'UserDamageReport',
    'ComCatModel',
    'GroupMemberUser',
    'Session',
    'Tenement',
    'AuthorizationCode',
    'Client',
    'Token'
]


# Order matters here.
MODELS = (
    Address,
    Tenement,
    User,
    Client,
    Token,
    AuthorizationCode,
    Session,
    UserBaseChart,
    UserConfiguration,
    UserMenu,
    UserDamageReport,
    GroupMemberUser
)


def create_tables():
    """Creates the tables for the ComCat database."""

    for model in MODELS:
        model.create_table()
