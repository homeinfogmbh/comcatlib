"""Emailing."""

from emaillib import Mailer

from comcatlib.config import get_config


__all__ = ["SENDER", "get_mailer"]


SENDER = "mieterapp@homeinfo.de"


def get_mailer() -> Mailer:
    """Returns the mailer."""

    return Mailer.from_config(get_config())
