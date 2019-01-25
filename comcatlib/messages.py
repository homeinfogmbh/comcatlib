"""Web API messages."""

from wsgilib import MessageFacility


__all__ = ['NO_SUCH_ACCOUNT', 'NO_SUCH_CUSTOMER']


COMCAT_MESSAGE_FACILITY = MessageFacility('/usr/local/etc/comcat.d/locales')
COMCAT_MESSAGE_DOMAIN = COMCAT_MESSAGE_FACILITY.domain('comcat')
COMCAT_MESSAGE = COMCAT_MESSAGE_DOMAIN.message
NO_SUCH_ACCOUNT = COMCAT_MESSAGE(
    'The requested account does not exists.', status=404)
NO_SUCH_CUSTOMER = COMCAT_MESSAGE(
    'The requested customer does not exists.', status=404)
SESSION_EXPIRED = COMCAT_MESSAGE('Session expired.', status=401)
ACCOUNT_LOCKED = COMCAT_MESSAGE('This account is locked.', status=401)
