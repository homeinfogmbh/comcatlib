"""Attachments-related messages."""

from wsgilib import JSONMessage


__all__ = ['NO_SUCH_ATTACHMENT']


NO_SUCH_ATTACHMENT = JSONMessage('No such attachment.', status=404)
