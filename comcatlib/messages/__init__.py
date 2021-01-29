"""Web API messages."""

from comcatlib.messages.clientreg import INVALID_UUID
from comcatlib.messages.clientreg import INVALID_NONCE
from comcatlib.messages.clientreg import MISSING_NONCE
from comcatlib.messages.files import NO_SUCH_FILE
from comcatlib.messages.files import QUOTA_EXCEEDED
from comcatlib.messages.news import NEWS_NOT_ENABLED
from comcatlib.messages.news import NO_SUCH_ARTICLE
from comcatlib.messages.news import NO_SUCH_ARTICLE_IMAGE
from comcatlib.messages.user import DUPLICATE_USER
from comcatlib.messages.user import INVALID_CREDENTIALS
from comcatlib.messages.user import MISSING_USER_ID
from comcatlib.messages.user import MISSING_USER_PW
from comcatlib.messages.user import NO_SUCH_USER
from comcatlib.messages.user import USER_ADDED
from comcatlib.messages.user import USER_DELETED
from comcatlib.messages.user import USER_EXPIRED
from comcatlib.messages.user import USER_LOCKED
from comcatlib.messages.user import USER_PATCHED


__all__ = [
    'INVALID_UUID',
    'INVALID_NONCE',
    'MISSING_NONCE',
    'NO_SUCH_FILE',
    'QUOTA_EXCEEDED',
    'NEWS_NOT_ENABLED',
    'NO_SUCH_ARTICLE',
    'NO_SUCH_ARTICLE_IMAGE',
    'DUPLICATE_USER',
    'INVALID_CREDENTIALS',
    'MISSING_USER_ID',
    'MISSING_USER_PW',
    'NO_SUCH_USER',
    'USER_ADDED',
    'USER_DELETED',
    'USER_EXPIRED',
    'USER_LOCKED',
    'USER_PATCHED'
]
