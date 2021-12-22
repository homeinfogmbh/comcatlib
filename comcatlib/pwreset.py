"""Password reset functions."""

from emaillib import EMail

from comcatlib.config import get_config
from comcatlib.email import get_mailer
from comcatlib.orm import PasswordResetNonce


__all__ = ['send_password_reset_email']


SENDER = 'comcat@homeinfo.de'
SUBJECT = 'Zurücksetzen Ihres Mieter-App Passworts'
TEMPLATE = '''Sehr geehrter Nutzer,

Sie haben das Zurücksetzen Ihres Mieter-App Passworts beantragt.
Bitte geben Sie das folgende Sicherheitstoken in Ihrer Mieterapp ein,
um Ihr Password zurückzusetzen.

Sicherheitstoken: {nonce.uuid.hex}

Sollten Sie kein Zurücksetzen Ihres Passwortes beantragt haben,
so ignorieren Sie bitte diese E-Mail.

Mit freundlichen Grüßen

Ihre {nonce.user.customer.name}
'''


def gen_email(nonce: PasswordResetNonce) -> EMail:
    """Generates a password reset email."""

    return EMail(
        (config := get_config()).get('pwreset', 'subject', fallback=SUBJECT),
        config.get('pwreset', 'sender', fallback=SENDER),
        nonce.user.email,
        plain=config.get('pwreset', 'template', fallback=TEMPLATE).format(
            nonce=nonce)
    )


def send_password_reset_email(nonce: PasswordResetNonce) -> bool:
    """Sends a password reset email."""

    return get_mailer().send([gen_email(nonce)])
