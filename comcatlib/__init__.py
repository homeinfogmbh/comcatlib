"""Comcat backend."""

from comcatlib.app import init_oauth_endpoints
from comcatlib.damage_report import list_ as list_damage_reports
from comcatlib.damage_report import submit as submit_damage_reports
from comcatlib.oauth import REQUIRE_OAUTH, SERVER, init_oauth
from comcatlib.orm import Address
from comcatlib.orm import UserBaseChart
from comcatlib.orm import UserConfiguration
from comcatlib.orm import UserDamageReport
from comcatlib.orm import UserMenu
from comcatlib.orm import GroupMemberUser
from comcatlib.orm import Tenement
from comcatlib.orm import User
from comcatlib.presentation import Presentation
from comcatlib.urlproxy import decode_url, encode_url, proxy_url


TEMPLATE_FOLDER = '/usr/local/share/comcatlib/'


__all__ = [
    'REQUIRE_OAUTH',
    'SERVER',
    'TEMPLATE_FOLDER',
    'init_oauth',
    'init_oauth_endpoints',
    'list_damage_reports',
    'submit_damage_reports',
    'decode_url',
    'encode_url',
    'proxy_url',
    'User',
    'UserBaseChart',
    'UserConfiguration',
    'UserMenu',
    'UserDamageReport',
    'Address',
    'GroupMemberUser',
    'Tenement',
    'Presentation'
]
