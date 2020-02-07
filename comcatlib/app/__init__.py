"""Backend for the smartphone apps."""

from comcatlib.app.auth import get_session_duration
from comcatlib.app.auth import authenticated
from comcatlib.app.contextlocals import CUSTOMER
from comcatlib.app.contextlocals import SESSION
from comcatlib.app.contextlocals import USER
from comcatlib.app.endpoints import init_oauth_endpoints


__all__ = [
    'CUSTOMER',
    'SESSION',
    'USER',
    'authenticated',
    'get_session_duration',
    'init_oauth_endpoints'
]
