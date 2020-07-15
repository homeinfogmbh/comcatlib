"""Object relational mappings."""


from comcatlib.orm.common import DATABASE, ComCatModel
from comcatlib.orm.content import UserBaseChart
from comcatlib.orm.content import UserConfiguration
from comcatlib.orm.content import UserMenu
from comcatlib.orm.damage_report import UserDamageReport
from comcatlib.orm.damage_report import DamageReportAttachment
from comcatlib.orm.files import add_file, File, Quota
from comcatlib.orm.group import GroupMemberUser
from comcatlib.orm.menu import BaseChartMenu
from comcatlib.orm.oauth import AuthorizationCode
from comcatlib.orm.oauth import Client
from comcatlib.orm.oauth import Token
from comcatlib.orm.tenant2tenant import UserTenantMessage
from comcatlib.orm.user import get_user, User


__all__ = [
    'DATABASE',
    'MODELS',
    'create_tables',
    'get_user',
    'add_file',
    'BaseChartMenu',
    'ComCatModel',
    'UserBaseChart',
    'UserConfiguration',
    'UserMenu',
    'UserDamageReport',
    'DamageReportAttachment',
    'File',
    'Quota',
    'GroupMemberUser',
    'AuthorizationCode',
    'Client',
    'Token',
    'UserTenantMessage',
    'User'
]


# Order matters here.
MODELS = (
    BaseChartMenu,
    User,
    Client,
    Token,
    AuthorizationCode,
    UserBaseChart,
    UserConfiguration,
    UserMenu,
    UserDamageReport,
    UserTenantMessage,
    GroupMemberUser,
    File,
    Quota
)


def create_tables():
    """Creates the tables for the ComCat database."""

    for model in MODELS:
        model.create_table()
