"""Registration related functions."""

from pathlib import Path
from typing import Iterator, Optional
from xml.etree.ElementTree import Element, SubElement, tostring

from emaillib import EMail
from mdb import Customer

from comcatlib.email import SENDER, get_mailer
from comcatlib.orm.registration import UserRegistration
from comcatlib.orm.registration import RegistrationNotificationEmails


__all__ = ['notify_customer', 'notify_user']


NOTIFICATION_SUBJECT = 'Neue Benutzerregistrierungen für Ihre App'
SUBJECT = 'Mieter-App'
USER_CONFIRM_TEMP = Path('/usr/local/etc/comcat.d/user-confirmation.temp')
USER_REG_TEMP = Path('/usr/local/etc/comcat.d/user-registration.temp')


def notify_customer(user_registration: UserRegistration) -> None:
    """Notify customer via email about a user registration event."""

    get_mailer().send(get_customer_emails(user_registration))


def notify_user(email: str, passwd: Optional[str] = None) -> None:
    """Sends a notification email to the registered email address."""

    get_mailer().send([
        EMail(SUBJECT, SENDER, email, plain=get_body(email, passwd))
    ])


def get_customer_emails(
        user_registration: UserRegistration
) -> Iterator[EMail]:
    """Yields emails to send."""

    html = tostring(
        to_html(user_registration), encoding='unicode', method='html'
    )

    for notification_email in RegistrationNotificationEmails.select().where(
            RegistrationNotificationEmails.customer ==
            user_registration.customer
    ):
        yield EMail(
            NOTIFICATION_SUBJECT, SENDER, notification_email.email, html=html
        )


def to_html(user_registration: UserRegistration) -> Element:
    """Converts user registrations into an HTML element."""

    html = Element('html')
    body = SubElement(html, 'body')
    h1 = SubElement(body, 'h1')
    h1.text = 'Neue Registrierung'
    p = SubElement(body, 'p')
    p.text = 'Folgender Benutzer hat sich für die App registriert:'
    SubElement(body, 'br')
    table = SubElement(body, 'table', attrs={'border': '1'})
    table.append(user_registration.to_html())
    p = SubElement(body, 'p')
    p.text = 'Mit freundlichen Grüßen'
    SubElement(body, 'br')
    p = SubElement(body, 'p')
    p.text = 'Ihre HOMEINFO GmbH'
    return html


def get_body(email: str, passwd: Optional[str] = None) -> str:
    """Returns the email body."""

    if passwd is None:
        with USER_REG_TEMP.open(encoding='utf-8') as file:
            return file.read()

    with USER_CONFIRM_TEMP.open(encoding='utf-8') as file:
        return file.read().format(name=email, passwd=passwd)
