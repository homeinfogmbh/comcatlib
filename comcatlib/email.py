"""Emailing."""

from emaillib import Mailer

from comcatlib.config import CONFIG


__all__ = ['MAILER', 'SENDER']


MAILER = Mailer.from_config(CONFIG)
SENDER = 'mieterapp@homeinfo.de'
