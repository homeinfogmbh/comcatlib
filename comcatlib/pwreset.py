"""Password reset functions."""

from emaillib import EMail

from comcatlib.config import get_config
from comcatlib.email import get_mailer
from comcatlib.orm import PasswordResetNonce


__all__ = ['send_new_password', 'send_password_reset_email']


PASSWORD_SENT_VIA_EMAIL = 'Ihr neues Passwort wurde Ihnen per E-Mail gesendet.'
SENDER = 'comcat@homeinfo.de'
SUBJECT = 'Zurücksetzen Ihres Mieter-App Passworts'
RESET_TEMPLATE = '''Sehr geehrter Nutzer,

Sie haben das Zurücksetzen Ihres Mieter-App Passworts beantragt.
Bitte besuchen Sie bitte den folgenden Link um Ihr Passwort zurückzusetzen:

https://pwreset.homeinfo.de/comcat/?nonce={nonce}

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


def send_new_password(recipient: str, passwd: str) -> None:
    """Send an email with a password to the recipient."""

    get_mailer().send([gen_new_pw_email(recipient, passwd)])


def send_password_reset_email(nonce: PasswordResetNonce) -> None:
    """Sends a password reset email."""

    get_mailer().send([gen_pw_reset_email(nonce)])


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
            nonce=nonce.uuid.hex
        )
    )
