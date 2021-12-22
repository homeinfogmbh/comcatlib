"""Object relational mappings."""

from comcatlib.orm.common import DATABASE
from comcatlib.orm.contactform import ContactEmails
from comcatlib.orm.content import UserBaseChart
from comcatlib.orm.content import UserConfiguration
from comcatlib.orm.content import UserMenu
from comcatlib.orm.damage_report import UserDamageReport
from comcatlib.orm.group import GroupMemberUser
from comcatlib.orm.menu import MenuBaseChart
from comcatlib.orm.nonces import AuthorizationNonce
from comcatlib.orm.nonces import EMailChangeNonce
from comcatlib.orm.nonces import PasswordResetNonce
from comcatlib.orm.oauth import AuthorizationCode
from comcatlib.orm.oauth import Client
from comcatlib.orm.oauth import Contact
from comcatlib.orm.oauth import GrantType
from comcatlib.orm.oauth import JWKS
from comcatlib.orm.oauth import RedirectURI
from comcatlib.orm.oauth import ResponseType
from comcatlib.orm.oauth import Scope
from comcatlib.orm.oauth import Token
from comcatlib.orm.registration import UserRegistration
from comcatlib.orm.registration import RegistrationNotificationEmails
from comcatlib.orm.settings import Settings
from comcatlib.orm.user import User


__all__ = [
    'DATABASE',
    'MODELS',
    'create_tables',
    'AuthorizationCode',
    'AuthorizationNonce',
    'Client',
    'Contact',
    'ContactEmails',
    'EMailChangeNonce',
    'GrantType',
    'GroupMemberUser',
    'JWKS',
    'MenuBaseChart',
    'PasswordResetNonce',
    'RedirectURI',
    'RegistrationNotificationEmails',
    'ResponseType',
    'Scope',
    'Settings',
    'Token',
    'User',
    'UserBaseChart',
    'UserConfiguration',
    'UserDamageReport',
    'UserMenu',
    'UserRegistration'
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
    Settings,
    Scope,
    Token,
    AuthorizationCode,
    # Nonces
    AuthorizationNonce,
    EMailChangeNonce,
    PasswordResetNonce,
    # User-related stuff.
    ContactEmails,
    RegistrationNotificationEmails,
    UserBaseChart,
    UserConfiguration,
    UserDamageReport,
    UserMenu,
    UserRegistration,
    # Misc
    MenuBaseChart
)


def create_tables():
    """Creates the tables for the ComCat database."""

    for model in MODELS:
        model.create_table()
