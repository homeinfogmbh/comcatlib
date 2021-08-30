"""ComCat configuration."""

from json import load

from configlib import loadcfg


__all__ = [
    'CONFIG',
    'ALLOWED_SESSION_DURATIONS',
    'DEFAULT_SESSION_DURATION',
    'OAUTH2'
]


CONFIG = loadcfg('comcat.conf')
ALLOWED_SESSION_DURATIONS = range(5, 31)
DEFAULT_SESSION_DURATION = 15


with open('/usr/local/etc/comcat.d/oauth2.json', 'r') as oauth2:
    OAUTH2 = load(oauth2)
