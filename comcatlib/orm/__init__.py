"""Object relational mappings."""


from comcatlib.orm.common import DATABASE, ComCatModel
from comcatlib.orm.content import UserBaseChart
from comcatlib.orm.content import UserConfiguration
from comcatlib.orm.content import UserMenu
from comcatlib.orm.damage_report import UserDamageReport
from comcatlib.orm.files import Quota, UserFile
from comcatlib.orm.group import GroupMemberUser
from comcatlib.orm.nonces import AuthorizationNonce
from comcatlib.orm.menu import BaseChartMenu
from comcatlib.orm.oauth import AuthorizationCode
from comcatlib.orm.oauth import Client
from comcatlib.orm.oauth import Contact
from comcatlib.orm.oauth import GrantType
from comcatlib.orm.oauth import JWKS
from comcatlib.orm.oauth import RedirectURI
from comcatlib.orm.oauth import ResponseType
from comcatlib.orm.oauth import Scope
from comcatlib.orm.oauth import Token
from comcatlib.orm.tenant2tenant import UserTenantMessage
from comcatlib.orm.user import get_user, User


__all__ = [
    'DATABASE',
    'MODELS',
    'create_tables',
    'get_user',
    'User',
    # OAuth
    'Client',
    'Contact',
    'GrantType',
    'GroupMemberUser',
    'JWKS',
    'RedirectURI',
    'ResponseType',
    'Scope',
    'Token',
    'AuthorizationCode',
    # Nonces
    'AuthorizationNonce',
    # User-related stuff.
    'UserBaseChart',
    'UserConfiguration',
    'UserDamageReport',
    'UserFile',
    'UserMenu',
    'UserTenantMessage',
    # Misc
    'BaseChartMenu',
    'Quota'
]


# Order matters here.
MODELS = (
    User,
    # OAuth
    Client,
    Contact,
    GrantType,
    GroupMemberUser,
    JWKS,
    RedirectURI,
    ResponseType,
    Scope,
    Token,
    AuthorizationCode,
    # Nonces
    AuthorizationNonce,
    # User-related stuff.
    UserBaseChart,
    UserConfiguration,
    UserDamageReport,
    UserFile,
    UserMenu,
    UserTenantMessage,
    # Misc
    BaseChartMenu,
    Quota
)


def create_tables():
    """Creates the tables for the ComCat database."""

    for model in MODELS:
        model.create_table()
