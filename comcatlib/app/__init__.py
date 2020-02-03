"""Backend for the smartphone apps."""

from comcatlib.app.auth import get_session_duration
from comcatlib.app.auth import authenticated
from comcatlib.app.contextlocals import CUSTOMER
from comcatlib.app.contextlocals import SESSION
from comcatlib.app.contextlocals import USER
from comcatlib.messages import SESSION_EXPIRED
from comcatlib.messages import USER_LOCKED
from comcatlib.messages import INVALID_CREDENTIALS
from comcatlib.messages import NO_ADDRESS_CONFIGURED


__all__ = [
    'CUSTOMER',
    'SESSION',
    'USER',
    'SESSION_EXPIRED',
    'USER_LOCKED',
    'INVALID_CREDENTIALS',
    'NO_ADDRESS_CONFIGURED',
    'authenticated',
    'get_session_duration'
]
