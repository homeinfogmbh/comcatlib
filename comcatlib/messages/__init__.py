"""Web API messages."""

from comcatlib.messages.address import ADDRESS_ADDED
from comcatlib.messages.address import ADDRESS_DELETED
from comcatlib.messages.address import INVALID_ADDRESS
from comcatlib.messages.address import MISSING_ADDRESS
from comcatlib.messages.address import NO_SUCH_ADDRESS
from comcatlib.messages.attachments import ATTACHMENT_ADDED
from comcatlib.messages.attachments import ATTACHMENT_DELETED
from comcatlib.messages.attachments import NO_SUCH_ATTACHMENT
from comcatlib.messages.base_chart_menu import BASE_CHART_MENU_ADDED
from comcatlib.messages.base_chart_menu import BASE_CHART_MENU_DELETED
from comcatlib.messages.base_chart_menu import NO_SUCH_BASE_CHART_MENU
from comcatlib.messages.clientreg import INVALID_UUID
from comcatlib.messages.clientreg import INVALID_NONCE
from comcatlib.messages.clientreg import MISSING_NONCE
from comcatlib.messages.damage_report import DAMAGE_REPORT_ALREADY_PROCESSED
from comcatlib.messages.damage_report import DAMAGE_REPORT_DELETED
from comcatlib.messages.damage_report import DAMAGE_REPORT_SUBMITTED
from comcatlib.messages.damage_report import NO_SUCH_DAMAGE_REPORT
from comcatlib.messages.files import NO_SUCH_FILE
from comcatlib.messages.files import QUOTA_EXCEEDED
from comcatlib.messages.news import NEWS_NOT_ENABLED
from comcatlib.messages.news import NO_SUCH_ARTICLE
from comcatlib.messages.news import NO_SUCH_ARTICLE_IMAGE
from comcatlib.messages.tenement import INVALID_TENEMENT
from comcatlib.messages.tenement import NO_SUCH_TENEMENT
from comcatlib.messages.tenement import TENEMENT_ADDED
from comcatlib.messages.tenement import TENEMENT_DELETED
from comcatlib.messages.tenement import TENEMENT_IN_USE
from comcatlib.messages.tenement import TENEMENT_PATCHED
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
    'ADDRESS_ADDED',
    'ATTACHMENT_DELETED',
    'ADDRESS_DELETED',
    'INVALID_ADDRESS',
    'MISSING_ADDRESS',
    'NO_SUCH_ADDRESS',
    'ATTACHMENT_ADDED',
    'NO_SUCH_ATTACHMENT',
    'BASE_CHART_MENU_ADDED',
    'BASE_CHART_MENU_DELETED',
    'NO_SUCH_BASE_CHART_MENU',
    'INVALID_UUID',
    'INVALID_NONCE',
    'MISSING_NONCE',
    'DAMAGE_REPORT_ALREADY_PROCESSED',
    'DAMAGE_REPORT_DELETED',
    'DAMAGE_REPORT_SUBMITTED',
    'NO_SUCH_DAMAGE_REPORT',
    'NO_SUCH_FILE',
    'QUOTA_EXCEEDED',
    'NEWS_NOT_ENABLED',
    'NO_SUCH_ARTICLE',
    'NO_SUCH_ARTICLE_IMAGE',
    'INVALID_TENEMENT',
    'NO_SUCH_TENEMENT',
    'TENEMENT_ADDED',
    'TENEMENT_DELETED',
    'TENEMENT_IN_USE',
    'TENEMENT_PATCHED',
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
