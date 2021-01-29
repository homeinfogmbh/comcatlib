"""Comcat backend."""

from comcatlib.app import init_oauth_endpoints
from comcatlib.localproxies import ADDRESS
from comcatlib.localproxies import CUSTOMER
from comcatlib.localproxies import TENEMENT
from comcatlib.localproxies import USER
from comcatlib.localproxies import get_user
from comcatlib.exceptions import DuplicateUser
from comcatlib.exceptions import InvalidAddress
from comcatlib.exceptions import UserExpired
from comcatlib.exceptions import UserLocked
from comcatlib.files import add_file
from comcatlib.oauth import REQUIRE_OAUTH, SERVER, init_oauth
from comcatlib.orm import AuthorizationNonce
from comcatlib.orm import GroupMemberUser
from comcatlib.orm import MenuBaseChart
from comcatlib.orm import Quota
from comcatlib.orm import User
from comcatlib.orm import UserBaseChart
from comcatlib.orm import UserConfiguration
from comcatlib.orm import UserDamageReport
from comcatlib.orm import UserFile
from comcatlib.orm import UserMenu
from comcatlib.presentation import Presentation
from comcatlib.urlproxy import decode_url, encode_url, proxy_url


__all__ = [
    'REQUIRE_OAUTH',
    'SERVER',
    'ADDRESS',
    'CUSTOMER',
    'TENEMENT',
    'USER',
    'DuplicateUser',
    'InvalidAddress',
    'UserExpired',
    'UserLocked',
    'add_file',
    'get_user',
    'init_app',
    'oauth',
    'decode_url',
    'encode_url',
    'proxy_url',
    'AuthorizationNonce',
    'GroupMemberUser',
    'MenuBaseChart',
    'Quota',
    'User',
    'UserBaseChart',
    'UserConfiguration',
    'UserDamageReport',
    'UserFile',
    'UserMenu',
    'Presentation'
]


def init_app(app):
    """Initializes a flask application with an OAuth 2.0
    authorization server and the respective endpoints.
    """

    init_oauth(app)
    init_oauth_endpoints(app)
