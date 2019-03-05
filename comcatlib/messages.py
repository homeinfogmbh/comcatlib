"""Web API messages."""

from wsgilib import MessageFacility


__all__ = [
    'NO_SUCH_ACCOUNT',
    'NO_SUCH_CUSTOMER',
    'SESSION_EXPIRED',
    'ACCOUNT_LOCKED',
    'ACCOUNT_ADDED',
    'ACCOUNT_DELETED',
    'ACCOUNT_PATCHED',
    'INVALID_CREDENTIALS',
    'NO_ADDRESS_CONFIGURED']


COMCAT_MESSAGE_FACILITY = MessageFacility('/usr/local/etc/comcat.d/locales')
COMCAT_MESSAGE_DOMAIN = COMCAT_MESSAGE_FACILITY.domain('comcat')
COMCAT_MESSAGE = COMCAT_MESSAGE_DOMAIN.message
NO_SUCH_ACCOUNT = COMCAT_MESSAGE(
    'The requested account does not exists.', status=404)
NO_SUCH_CUSTOMER = COMCAT_MESSAGE(
    'The requested customer does not exists.', status=404)
SESSION_EXPIRED = COMCAT_MESSAGE('Session expired.', status=401)
ACCOUNT_LOCKED = COMCAT_MESSAGE('This account is locked.', status=401)
ACCOUNT_ADDED = COMCAT_MESSAGE('The account has been added.', status=201)
ACCOUNT_DELETED = COMCAT_MESSAGE('The account has been deleted.', status=200)
ACCOUNT_PATCHED = COMCAT_MESSAGE('The account has been modified.', status=200)
INVALID_CREDENTIALS = COMCAT_MESSAGE(
    'User name and/or password inclorrect.', status=400)
NO_ADDRESS_CONFIGURED = COMCAT_MESSAGE(
    'Account has no address configured.', status=400)
NEWS_NOT_ENABLED = COMCAT_MESSAGE('Module "news" is not enabled.', status=403)
NO_SUCH_ARTICLE = COMCAT_MESSAGE(
    'The requested articles does not exists.', status=404)
NO_SUCH_ARTICLE_IMAGE = COMCAT_MESSAGE(
    'The requested article image does not exists.', status=404)
