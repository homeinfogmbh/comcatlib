"""Web API messages."""

from wsgilib import JSONMessage


__all__ = [
    'NO_SUCH_ACCOUNT',
    'NO_SUCH_CUSTOMER',
    'SESSION_EXPIRED',
    'ACCOUNT_LOCKED',
    'ACCOUNT_ADDED',
    'ACCOUNT_DELETED',
    'ACCOUNT_PATCHED',
    'INVALID_CREDENTIALS',
    'NO_ADDRESS_CONFIGURED',
    'ADDRESS_ADDED',
    'ADDRESS_DELETED',
    'INVALID_ADDRESS_VALUE',
    'NO_SUCH_ADDRESS',
    'TENEMENT_ADDED',
    'TENEMENT_DELETED',
    'NO_SUCH_TENEMENT',
    'TENEMENT_PATCHED',
    'INVALID_TENEMENT_VALUE']


NO_SUCH_ACCOUNT = JSONMessage(
    'The requested account does not exists.', status=404)
NO_SUCH_CUSTOMER = JSONMessage(
    'The requested customer does not exists.', status=404)
SESSION_EXPIRED = JSONMessage('Session expired.', status=401)
ACCOUNT_LOCKED = JSONMessage('This account is locked.', status=401)
ACCOUNT_ADDED = JSONMessage('The account has been added.', status=201)
ACCOUNT_DELETED = JSONMessage('The account has been deleted.', status=200)
ACCOUNT_PATCHED = JSONMessage('The account has been modified.', status=200)
INVALID_CREDENTIALS = JSONMessage(
    'User name and/or password inclorrect.', status=400)
NO_ADDRESS_CONFIGURED = JSONMessage(
    'Account has no address configured.', status=400)
NEWS_NOT_ENABLED = JSONMessage('Module "news" is not enabled.', status=403)
NO_SUCH_ARTICLE = JSONMessage(
    'The requested articles does not exists.', status=404)
NO_SUCH_ARTICLE_IMAGE = JSONMessage(
    'The requested article image does not exists.', status=404)
ADDRESS_ADDED = JSONMessage('The address has been added.', status=201)
ADDRESS_DELETED = JSONMessage('The address has been deleted.', status=200)
INVALID_ADDRESS_VALUE = JSONMessage('Invalid value for address.', status=400)
NO_SUCH_ADDRESS = JSONMessage(
    'The requested address does not eixst.', status=404)
TENEMENT_ADDED = JSONMessage('The tenement has been added.', status=201)
TENEMENT_DELETED = JSONMessage('The tenement has been deleted.', status=200)
NO_SUCH_TENEMENT = JSONMessage(
    'The requested tenement does not eixst.', status=404)
TENEMENT_PATCHED = JSONMessage(
    'The requested tenement has been patched.', status=404)
INVALID_TENEMENT_VALUE = JSONMessage('Invalid value for tenement.', status=400)
