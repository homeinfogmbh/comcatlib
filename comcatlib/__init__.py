"""Comcat backend."""

from comcatlib.auth import authenticated
from comcatlib.contextlocals import ACCOUNT, CUSTOMER, SESSION
from comcatlib.damage_report import list_ as list_damage_reports
from comcatlib.damage_report import submit as submit_damage_reports
from comcatlib.facebook import get_accounts as get_facebook_accounts
from comcatlib.facebook import get_posts as get_facebook_posts
from comcatlib.functions import get_account, get_session_duration
from comcatlib.orm import Account
from comcatlib.orm import AccountBaseChart
from comcatlib.orm import AccountConfiguration
from comcatlib.orm import AccountDamageReport
from comcatlib.orm import AccountMenu
from comcatlib.orm import Address
from comcatlib.orm import GroupMemberAccount
from comcatlib.orm import Session
from comcatlib.orm import Tenement
from comcatlib.presentation import Presentation
from comcatlib.urlproxy import decode_url, encode_url, proxy_url


__all__ = [
    'ACCOUNT',
    'CUSTOMER',
    'SESSION',
    'authenticated',
    'get_account',
    'get_session_duration',
    'list_damage_reports',
    'submit_damage_reports',
    'get_facebook_accounts',
    'get_facebook_posts',
    'decode_url',
    'encode_url',
    'proxy_url',
    'Account',
    'AccountBaseChart',
    'AccountConfiguration',
    'AccountMenu',
    'AccountDamageReport',
    'Address',
    'GroupMemberAccount',
    'Session',
    'Tenement',
    'Presentation']
