"""ComCat configuration."""

from functools import cache, partial
from pathlib import Path

from configlib import load_config


__all__ = [
    'CONFIG_FILE',
    'ALLOWED_SESSION_DURATIONS',
    'DEFAULT_SESSION_DURATION',
    'get_config',
    'get_oauth2'
]


CONFIG_FILE = 'comcat.conf'
ALLOWED_SESSION_DURATIONS = range(5, 31)
DEFAULT_SESSION_DURATION = 15
OAUTH2_JSON = Path('/usr/local/etc/comcat.d/oauth2.json')


load_config = cache(load_config)
get_config = partial(load_config, CONFIG_FILE)
get_oauth2 = partial(load_config, OAUTH2_JSON)
