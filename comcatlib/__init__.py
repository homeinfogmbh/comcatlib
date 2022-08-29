"""ComCat backend."""

from comcatlib.app import init_oauth_endpoints
from comcatlib.config import get_config
from comcatlib.contactform import send_contact_mails
from comcatlib.email_change import request_email_change, confirm_email_change
from comcatlib.exceptions import AlreadyRegistered
from comcatlib.exceptions import DuplicateUser
from comcatlib.exceptions import InvalidAddress
from comcatlib.exceptions import InvalidPassword
from comcatlib.exceptions import NonceUsed
from comcatlib.exceptions import PasswordResetPending
from comcatlib.exceptions import QuotaExceeded
from comcatlib.exceptions import UserExpired
from comcatlib.exceptions import UserLocked
from comcatlib.fcm import APP_NAME
from comcatlib.fcm import CAPTIONS
from comcatlib.fcm import URLCode
from comcatlib.fcm import delete_tokens
from comcatlib.fcm import expand_groups
from comcatlib.fcm import get_tokens
from comcatlib.fcm import init as init_fcm
from comcatlib.fcm import multicast_base_chart
from comcatlib.fcm import multicast_customer_event
from comcatlib.fcm import multicast_message
from comcatlib.functions import get_group_ids, get_groups_lineage, logout
from comcatlib.localproxies import ADDRESS
from comcatlib.localproxies import CUSTOMER
from comcatlib.localproxies import TENEMENT
from comcatlib.localproxies import USER
from comcatlib.oauth2 import REQUIRE_OAUTH, Token
from comcatlib.registration import notify_customer, notify_user
from comcatlib.orm import DATABASE
from comcatlib.orm import AuthorizationNonce
from comcatlib.orm import EMailChangeNonce
from comcatlib.orm import FCMToken
from comcatlib.orm import GroupMemberUser
from comcatlib.orm import Menu
from comcatlib.orm import MenuBaseChart
from comcatlib.orm import PasswordResetNonce
from comcatlib.orm import RegistrationNotificationEmails
from comcatlib.orm import Settings
from comcatlib.orm import User
from comcatlib.orm import UserBaseChart
from comcatlib.orm import UserConfiguration
from comcatlib.orm import UserDamageReport
from comcatlib.orm import UserMenu
from comcatlib.orm import UserRegistration
from comcatlib.presentation import Presentation
from comcatlib.pwgen import genpw
from comcatlib.pwreset import send_new_password, send_password_reset_email
from comcatlib.urlproxy import decode_url, encode_url, proxy_url


__all__ = [
    'ADDRESS',
    'APP_NAME',
    'CAPTIONS',
    'CUSTOMER',
    'DATABASE',
    'REQUIRE_OAUTH',
    'TENEMENT',
    'USER',
    'AlreadyRegistered',
    'DuplicateUser',
    'InvalidAddress',
    'InvalidPassword',
    'NonceUsed',
    'PasswordResetPending',
    'QuotaExceeded',
    'UserExpired',
    'UserLocked',
    'confirm_email_change',
    'decode_url',
    'delete_tokens',
    'encode_url',
    'expand_groups',
    'genpw',
    'get_config',
    'get_group_ids',
    'get_groups_lineage',
    'get_tokens',
    'init_fcm',
    'init_oauth_endpoints',
    'logout',
    'multicast_base_chart',
    'multicast_customer_event',
    'multicast_message',
    'notify_customer',
    'notify_user',
    'proxy_url',
    'request_email_change',
    'send_contact_mails',
    'send_new_password',
    'send_password_reset_email',
    'AuthorizationNonce',
    'EMailChangeNonce',
    'FCMToken',
    'GroupMemberUser',
    'Menu',
    'MenuBaseChart',
    'PasswordResetNonce',
    'RegistrationNotificationEmails',
    'Settings',
    'Token',
    'URLCode',
    'User',
    'UserBaseChart',
    'UserConfiguration',
    'UserDamageReport',
    'UserMenu',
    'UserRegistration',
    'Presentation'
]
