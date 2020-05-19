"""News-related messages."""

from wsgilib import JSONMessage


__all__ = ['NEWS_NOT_ENABLED', 'NO_SUCH_ARTICLE', 'NO_SUCH_ARTICLE_IMAGE']


NEWS_NOT_ENABLED = JSONMessage('Module "news" is not enabled.', status=403)
NO_SUCH_ARTICLE = JSONMessage(
    'The requested articles does not exists.', status=404)
NO_SUCH_ARTICLE_IMAGE = JSONMessage(
    'The requested article image does not exists.', status=404)
