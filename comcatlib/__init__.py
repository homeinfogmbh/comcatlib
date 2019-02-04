"""Comcat backend."""

from comcatlib.auth import authenticated
from comcatlib.contextlocals import ACCOUNT, CUSTOMER, SESSION
from comcatlib.damage_report import list_ as list_damage_reports
from comcatlib.damage_report import submit as submit_damage_reports
from comcatlib.functions import get_session_duration
from comcatlib.orm import Account, AccountDamageReport, Session
from comcatlib.urlproxy import decode_url, encode_url, proxy_url


__all__ = [
    'ACCOUNT',
    'CUSTOMER',
    'SESSION',
    'authenticated',
    'get_session_duration',
    'list_damage_reports',
    'submit_damage_reports',
    'decode_url',
    'encode_url',
    'proxy_url',
    'Account',
    'AccountDamageReport',
    'Session']
