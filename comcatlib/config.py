"""ComCat configuration."""

from functools import cache, partial
from json import load
from pathlib import Path

from configlib import load_config


__all__ = [
    'CONFIG_FILE',
    'ALLOWED_SESSION_DURATIONS',
    'DEFAULT_SESSION_DURATION',
    'OAUTH2',
    'get_config'
]


CONFIG_FILE = 'comcat.conf'
ALLOWED_SESSION_DURATIONS = range(5, 31)
DEFAULT_SESSION_DURATION = 15
OAUTH2_JSON = Path('/usr/local/etc/comcat.d/oauth2.json')


get_config = partial(cache(load_config), CONFIG_FILE)


with OAUTH2_JSON.open('r', encoding='utf-8') as oauth2:
    OAUTH2 = load(oauth2)
