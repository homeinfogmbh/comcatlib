"""Web API messages."""

from comcatlib.messages.address import ADDRESS_ADDED
from comcatlib.messages.address import ADDRESS_DELETED
from comcatlib.messages.address import INVALID_ADDRESS
from comcatlib.messages.address import MISSING_ADDRESS
from comcatlib.messages.address import NO_SUCH_ADDRESS
from comcatlib.messages.attachments import ATTACHMENT_ADDED
from comcatlib.messages.attachments import ATTACHMENT_DELETED
from comcatlib.messages.attachments import NO_SUCH_ATTACHMENT
from comcatlib.messages.damage_report import DAMAGE_REPORT_SUBMITTED
from comcatlib.messages.damage_report import NO_SUCH_DAMAGE_REPORT
from comcatlib.messages.files import NO_SUCH_FILE
from comcatlib.messages.files import QUOTA_EXCEEDED
from comcatlib.messages.login import INVALID_CREDENTIALS
from comcatlib.messages.login import MISSING_PASSWORD
from comcatlib.messages.news import NEWS_NOT_ENABLED
from comcatlib.messages.news import NO_SUCH_ARTICLE
from comcatlib.messages.news import NO_SUCH_ARTICLE_IMAGE
from comcatlib.messages.session import NOT_LOGGED_IN
from comcatlib.messages.session import SESSION_EXPIRED
from comcatlib.messages.tenement import INVALID_TENEMENT
from comcatlib.messages.tenement import NO_SUCH_TENEMENT
from comcatlib.messages.tenement import TENEMENT_ADDED
from comcatlib.messages.tenement import TENEMENT_DELETED
from comcatlib.messages.tenement import TENEMENT_PATCHED
from comcatlib.messages.user import NO_SUCH_CUSTOMER
from comcatlib.messages.user import NO_SUCH_USER
from comcatlib.messages.user import NO_USER_SPECIFIED
from comcatlib.messages.user import USER_ADDED
from comcatlib.messages.user import USER_DELETED
from comcatlib.messages.user import USER_LOCKED
from comcatlib.messages.user import USER_PATCHED


__all__ = [
    'ADDRESS_ADDED',
    'ATTACHMENT_DELETED',
    'ADDRESS_DELETED',
    'INVALID_ADDRESS',
    'MISSING_ADDRESS',
    'NO_SUCH_ADDRESS',
    'ATTACHMENT_ADDED',
    'NO_SUCH_ATTACHMENT',
    'DAMAGE_REPORT_SUBMITTED',
    'NO_SUCH_DAMAGE_REPORT',
    'NO_SUCH_FILE',
    'QUOTA_EXCEEDED',
    'INVALID_CREDENTIALS',
    'MISSING_PASSWORD',
    'NEWS_NOT_ENABLED',
    'NO_SUCH_ARTICLE',
    'NO_SUCH_ARTICLE_IMAGE',
    'NOT_LOGGED_IN',
    'SESSION_EXPIRED',
    'INVALID_TENEMENT',
    'NO_SUCH_TENEMENT',
    'TENEMENT_ADDED',
    'TENEMENT_DELETED',
    'TENEMENT_PATCHED',
    'NO_SUCH_CUSTOMER',
    'NO_SUCH_USER',
    'NO_USER_SPECIFIED',
    'USER_ADDED',
    'USER_DELETED',
    'USER_LOCKED',
    'USER_PATCHED'
]
