"""ComCat configuration."""

from configlib import loadcfg


__all__ = ['CONFIG', 'ALLOWED_SESSION_DURATIONS', 'DEFAULT_SESSION_DURATION']


CONFIG = loadcfg('comcat.conf')
ALLOWED_SESSION_DURATIONS = range(5, 31)
DEFAULT_SESSION_DURATION = 15
