"""Web API messages."""

from comcatlib.messages.news import NEWS_NOT_ENABLED
from comcatlib.messages.news import NO_SUCH_ARTICLE
from comcatlib.messages.news import NO_SUCH_ARTICLE_IMAGE
from comcatlib.messages.user import DUPLICATE_USER
from comcatlib.messages.user import MISSING_USER_PW
from comcatlib.messages.user import NO_SUCH_USER
from comcatlib.messages.user import USER_ADDED
from comcatlib.messages.user import USER_DELETED
from comcatlib.messages.user import USER_PATCHED


__all__ = [
    'NEWS_NOT_ENABLED',
    'NO_SUCH_ARTICLE',
    'NO_SUCH_ARTICLE_IMAGE',
    'DUPLICATE_USER',
    'MISSING_USER_PW',
    'NO_SUCH_USER',
    'USER_ADDED',
    'USER_DELETED',
    'USER_PATCHED'
]
