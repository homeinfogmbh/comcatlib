"""ComCat configuration."""

from json import load
from pathlib import Path

from configlib import loadcfg


__all__ = [
    'CONFIG',
    'ALLOWED_SESSION_DURATIONS',
    'DEFAULT_SESSION_DURATION',
    'OAUTH2',
    'USER_REG_TEMP'
]


CONFIG = loadcfg('comcat.conf')
ALLOWED_SESSION_DURATIONS = range(5, 31)
DEFAULT_SESSION_DURATION = 15
USER_REG_TEMP = Path('/usr/local/etc/comcat.d/userreg.temp')


with open('/usr/local/etc/comcat.d/oauth2.json', 'r') as oauth2:
    OAUTH2 = load(oauth2)
