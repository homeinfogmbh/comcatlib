"""Comcat backend."""

from comcatlib.auth import authenticated
from comcatlib.contextlocals import ACCOUNT, CUSTOMER, SESSION
from comcatlib.damage_report import list_ as list_damage_reports
from comcatlib.damage_report import submit as submit_damage_reports
from comcatlib.facebook import get_posts as get_facebook_posts
from comcatlib.functions import get_session_duration
from comcatlib.orm import Account, Session
from comcatlib.urlproxy import decode_url, encode_url, proxy_url


__all__ = [
    'ACCOUNT',
    'CUSTOMER',
    'SESSION',
    'authenticated',
    'get_session_duration',
    'list_damage_reports',
    'submit_damage_reports',
    'get_facebook_posts',
    'decode_url',
    'encode_url',
    'proxy_url',
    'Account',
    'Session']
