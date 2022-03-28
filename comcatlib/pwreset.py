"""Password reset functions."""

from uuid import UUID

from emaillib import EMail
from wsgilib import JSONMessage

from comcatlib.config import get_config
from comcatlib.email import get_mailer
from comcatlib.exceptions import NonceUsed
from comcatlib.orm import PasswordResetNonce
from comcatlib.pwgen import genpw


__all__ = ['send_password_reset_email', 'reset_password']


PASSWORD_SENT_VIA_EMAIL = 'Ihr neues Passwort wurde Ihnen per E-Mail gesendet.'
SENDER = 'comcat@homeinfo.de'
SUBJECT = 'Zurücksetzen Ihres Mieter-App Passworts'
RESET_TEMPLATE = '''Sehr geehrter Nutzer,

Sie haben das Zurücksetzen Ihres Mieter-App Passworts beantragt.
Bitte besuchen Sie bitte den folgenden Link um Ihr Passwort zurückzusetzen:

https://comcat.homeinfo.de/reset-pw?token={token}

Sollten Sie kein Zurücksetzen Ihres Passwortes beantragt haben,
so ignorieren Sie bitte diese E-Mail.

Mit freundlichen Grüßen

Ihre {customer}
'''
NEW_PW_TEMPLATE = '''Sehr geehrter Nutzer,

Sie haben das Zurücksetzen Ihres Mieter-App Passworts beantragt.

Ihr neues Passwort lautet: {passwd}

Mit freundlichen Grüßen

Ihre {customer}
'''


def send_password_reset_email(nonce: PasswordResetNonce) -> None:
    """Sends a password reset email."""

    get_mailer().send([gen_pw_reset_email(nonce)])


def reset_password(nonce: str) -> JSONMessage:
    """Reset the password for the given user."""

    try:
        uuid = UUID(nonce)
    except ValueError:
        return JSONMessage('Invalid UUID.')

    try:
        nonce = PasswordResetNonce.use(uuid)
    except NonceUsed:
        return JSONMessage('Invalid nonce.')

    nonce.user.passwd = passwd = genpw()
    nonce.user.save()
    send_new_password(nonce.user, passwd)
    return JSONMessage('New password sent.')


def send_new_password(recipient: str, passwd: str) -> None:
    """Send an email with a password to the recipient."""

    get_mailer().send([gen_new_pw_email(recipient, passwd)])


def gen_new_pw_email(recipient: str, passwd: str) -> EMail:
    """Generates an email containing a user's new password."""

    return EMail(
        (config := get_config()).get('pwreset', 'subject', fallback=SUBJECT),
        config.get('pwreset', 'sender', fallback=SENDER),
        recipient,
        plain=NEW_PW_TEMPLATE.format(passwd=passwd)
    )


def gen_pw_reset_email(nonce: PasswordResetNonce) -> EMail:
    """Generates a password reset email."""

    return EMail(
        (config := get_config()).get('pwreset', 'subject', fallback=SUBJECT),
        config.get('pwreset', 'sender', fallback=SENDER),
        nonce.user.email,
        plain=RESET_TEMPLATE.format(
            customer=nonce.user.customer.name,
            token=nonce.uuid.hex
        )
    )
