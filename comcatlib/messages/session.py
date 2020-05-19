"""Session-related messages."""

from wsgilib import JSONMessage


__all__ = ['NOT_LOGGED_IN', 'SESSION_EXPIRED']


NOT_LOGGED_IN = JSONMessage('You are not logged-in.', status=401)
SESSION_EXPIRED = JSONMessage('Session expired.', status=401)
