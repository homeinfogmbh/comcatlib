"""Emailing."""

from pathlib import Path

from emaillib import EMail, Mailer

from comcatlib.config import CONFIG


__all__ = [
    'MAILER',
    'USER_REG_SENDER',
    'USER_REG_SUBJECT',
    'USER_REG_TEMP',
    'make_user_registration_email'
]


MAILER = Mailer.from_config(CONFIG)
USER_REG_SENDER = 'noreply@homeinfo.de'
USER_REG_SUBJECT = 'Mieter-App'
USER_REG_TEMP = Path('/usr/local/etc/comcat.d/userreg.temp')


def make_user_registration_email(email: str, login: int, passwd: str) -> EMail:
    """Creates a user registration email."""

    with USER_REG_TEMP.open() as file:
        template = file.read()

    text = template.format(name=login, passwd=passwd)
    return EMail(USER_REG_SUBJECT, USER_REG_SENDER, email, plain=text)
