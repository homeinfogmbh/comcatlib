"""Object relational mappings."""

from comcatlib.orm.common import DATABASE
from comcatlib.orm.contactform import ContactEmails
from comcatlib.orm.content import UserBaseChart
from comcatlib.orm.content import UserConfiguration
from comcatlib.orm.content import UserMenu
from comcatlib.orm.damage_report import UserDamageReport
from comcatlib.orm.fcm import FCMToken
from comcatlib.orm.group import GroupMemberUser
from comcatlib.orm.menu import Menu, MenuBaseChart
from comcatlib.orm.nonces import AuthorizationNonce
from comcatlib.orm.nonces import EMailChangeNonce
from comcatlib.orm.nonces import PasswordResetNonce
from comcatlib.orm.registration import UserRegistration
from comcatlib.orm.registration import RegistrationNotificationEmails
from comcatlib.orm.settings import Settings
from comcatlib.orm.user import User


__all__ = [
    'DATABASE',
    'MODELS',
    'create_tables',
    'AuthorizationNonce',
    'ContactEmails',
    'EMailChangeNonce',
    'FCMToken',
    'GroupMemberUser',
    'Menu',
    'MenuBaseChart',
    'PasswordResetNonce',
    'RegistrationNotificationEmails',
    'Settings',
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
    Settings,
    GroupMemberUser,
    # Nonces
    AuthorizationNonce,
    EMailChangeNonce,
    PasswordResetNonce,
    # User-related stuff.
    ContactEmails,
    FCMToken,
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
