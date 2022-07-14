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
from comcatlib.orm.reports import OfferReport
from comcatlib.orm.reports import ResponseReport
from comcatlib.orm.reports import TopicReport
from comcatlib.orm.reports import UserEventReport
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
    'GroupMemberUser',
    'MenuBaseChart',
    'OfferReport',
    'PasswordResetNonce',
    'RegistrationNotificationEmails',
    'ResponseReport',
    'Settings',
    'TopicReport',
    'User',
    'UserBaseChart',
    'UserConfiguration',
    'UserDamageReport',
    'UserEventReport',
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
