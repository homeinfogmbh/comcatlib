'''Firebase API client.'''

from firebase import Firebase

from comcatlib.config import get_config


__all__ = ['FIREBASE']


def get_firebase_config() -> dict[str, str]:
    """Returns the firebase config as dict."""

    return dict(get_config()['firebase'])


FIREBASE = Firebase(get_firebase_config())
