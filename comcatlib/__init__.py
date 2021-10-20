"""Comcat backend."""

from comcatlib.app import init_oauth_endpoints
from comcatlib.config import CONFIG
from comcatlib.contactform import send_contact_mails
from comcatlib.exceptions import AlreadyRegistered
from comcatlib.exceptions import DuplicateUser
from comcatlib.exceptions import InvalidAddress
from comcatlib.exceptions import QuotaExceeded
from comcatlib.exceptions import UserExpired
from comcatlib.exceptions import UserLocked
from comcatlib.localproxies import ADDRESS
from comcatlib.localproxies import CUSTOMER
from comcatlib.localproxies import TENEMENT
from comcatlib.localproxies import USER
from comcatlib.localproxies import get_user
from comcatlib.oauth import REQUIRE_OAUTH, SERVER, init_oauth
from comcatlib.registration import notify_customer, notify_user
from comcatlib.orm import DATABASE
from comcatlib.orm import AuthorizationNonce
from comcatlib.orm import EMailChangeNonce
from comcatlib.orm import GroupMemberUser
from comcatlib.orm import MenuBaseChart
from comcatlib.orm import RegistrationNotificationEmails
from comcatlib.orm import Settings
from comcatlib.orm import Token
from comcatlib.orm import User
from comcatlib.orm import UserBaseChart
from comcatlib.orm import UserConfiguration
from comcatlib.orm import UserDamageReport
from comcatlib.orm import UserMenu
from comcatlib.orm import UserRegistration
from comcatlib.presentation import Presentation
from comcatlib.pwgen import genpw
from comcatlib.urlproxy import decode_url, encode_url, proxy_url


__all__ = [
    'CONFIG',
    'REQUIRE_OAUTH',
    'SERVER',
    'ADDRESS',
    'CUSTOMER',
    'DATABASE',
    'TENEMENT',
    'USER',
    'AlreadyRegistered',
    'DuplicateUser',
    'InvalidAddress',
    'QuotaExceeded',
    'UserExpired',
    'UserLocked',
    'decode_url',
    'encode_url',
    'genpw',
    'get_user',
    'init_app',
    'notify_customer',
    'notify_user',
    'oauth',
    'proxy_url',
    'send_contact_mails',
    'AuthorizationNonce',
    'EMailChangeNonce',
    'GroupMemberUser',
    'MenuBaseChart',
    'RegistrationNotificationEmails',
    'Settings',
    'Token',
    'User',
    'UserBaseChart',
    'UserConfiguration',
    'UserDamageReport',
    'UserMenu',
    'UserRegistration',
    'Presentation'
]


def init_app(app):
    """Initializes a flask application with an OAuth 2.0
    authorization server and the respective endpoints.
    """

    init_oauth(app)
    init_oauth_endpoints(app)
