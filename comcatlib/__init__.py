"""Comcat backend."""

from comcatlib.app import init_oauth_endpoints
from comcatlib.damage_report import list_ as list_damage_reports
from comcatlib.damage_report import submit as submit_damage_reports
from comcatlib.oauth import REQUIRE_OAUTH, SERVER, init_oauth
from comcatlib.orm import BaseChartMenu
from comcatlib.orm import File, Quota
from comcatlib.orm import GroupMemberUser
from comcatlib.orm import User
from comcatlib.orm import UserBaseChart
from comcatlib.orm import UserConfiguration
from comcatlib.orm import UserDamageReport, DamageReportAttachment
from comcatlib.orm import UserMenu
from comcatlib.presentation import Presentation
from comcatlib.urlproxy import decode_url, encode_url, proxy_url


__all__ = [
    'REQUIRE_OAUTH',
    'SERVER',
    'init_app',
    'list_damage_reports',
    'submit_damage_reports',
    'decode_url',
    'encode_url',
    'proxy_url',
    'BaseChartMenu',
    'File',
    'Quota',
    'GroupMemberUser',
    'User',
    'UserBaseChart',
    'UserConfiguration',
    'UserDamageReport',
    'DamageReportAttachment',
    'UserMenu',
    'Presentation'
]


def init_app(app):
    """Initializes a flask application with an OAuth 2.0
    authorization server and the respective endpoints.
    """

    init_oauth(app)
    init_oauth_endpoints(app)
