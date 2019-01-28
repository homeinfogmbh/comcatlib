"""Comcat backend."""

from comcatlib.auth import authenticated
from comcatlib.functions import get_session_duration
from comcatlib.orm import Account


__all__ = ['authenticated', 'get_session_duration', 'Account']
