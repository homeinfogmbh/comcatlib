'''Firebase API client.'''

from firebase import Firebase

from comcatlib.config import get_config


__all__ = ['get_firebase']


def get_firebase() -> Firebase:
    """Returns the firebase config as dict."""

    return Firebase(get_config()['firebase'])
