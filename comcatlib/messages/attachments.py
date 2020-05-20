"""Attachments-related messages."""

from wsgilib import JSONMessage


__all__ = ['ATTACHMENT_ADDED', 'ATTACHMENT_DELETED', 'NO_SUCH_ATTACHMENT']


ATTACHMENT_ADDED = JSONMessage('Attachment added.', status=201)
ATTACHMENT_DELETED = JSONMessage('Attachment deleted.', status=200)
NO_SUCH_ATTACHMENT = JSONMessage('No such attachment.', status=404)
