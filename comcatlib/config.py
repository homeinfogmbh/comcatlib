"""ComCat configuration."""

from json import load
from pathlib import Path

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
OAUTH2_JSON = Path('/usr/local/etc/comcat.d/oauth2.json')


with OAUTH2_JSON.open('r', encoding='utf-8') as oauth2:
    OAUTH2 = load(oauth2)
