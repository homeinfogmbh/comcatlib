"""Comcat backend."""

from comcatlib.auth import authenticated
from comcatlib.contextlocals import ACCOUNT, CUSTOMER, SESSION
from comcatlib.functions import get_session_duration
from comcatlib.orm import Account


__all__ = [
    'ACCOUNT',
    'CUSTOMER',
    'SESSION',
    'authenticated',
    'get_session_duration',
    'Account']
