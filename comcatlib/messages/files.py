"""Files-related messages."""

from wsgilib import JSONMessage


__all__ = ['NO_SUCH_FILE', 'QUOTA_EXCEEDED']


NO_SUCH_FILE = JSONMessage('No such file.', status=404)
QUOTA_EXCEEDED = JSONMessage('File quota exceeded.', status=406)
