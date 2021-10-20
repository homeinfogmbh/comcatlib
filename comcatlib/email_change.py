"""Handle email changes."""

from uuid import UUID
from xml.etree.ElementTree import Element, SubElement, tostring

from emaillib import EMail

from comcatlib.email import MAILER, SENDER
from comcatlib.orm import EMailChangeNonce, User


__all__ = ['request_email_change', 'confirm_email_change']


SUBJECT = 'Änderung Ihrer E-Mail Adresse in der Mieter-App'
URL = 'https://comcat.homeinfo.de/confirm-email/{}'


# pylint: disable=C0103
def get_html(user: User, nonce: str) -> Element:
    """Returns an HTML element."""

    html = Element('html')
    header = SubElement(html, 'header')
    SubElement(header, 'meta', attrib={'charset': 'UTF-8'})
    body = SubElement(html, 'body')
    h1 = SubElement(body, 'h1')
    h1.text = SUBJECT
    p = SubElement(body, 'p')
    p.text = f'Sehr geehrte/r {user.name},'
    SubElement(body, 'br')
    p = SubElement(body, 'p')
    p.text = (
        'Bitte folgen Sie dem unten stehenden Link um Ihre E-Mail Adresse '
        'in der Mieter-App zu bestätigen.'
    )
    SubElement(body, 'br')
    a = SubElement(body, 'a', attrib={'href': (url := URL.format(nonce))})
    a.text = url
    SubElement(body, 'br')
    p = SubElement(body, 'p')
    p.text = 'Mit freundlichen Grüßen'
    SubElement(body, 'br')
    p = SubElement(body, 'p')
    p.text = 'Ihre HOMEINFO GmbH'
    return html


def get_email(user: User, email: str, nonce: str) -> EMail:
    """Returns an email to the user's new email address."""

    return EMail(SUBJECT, SENDER, email, html=tostring(get_html(user, nonce)))


def request_email_change(user: User, email: str) -> bool:
    """Changes the user email."""

    nonce = EMailChangeNonce.add(user, email)
    return MAILER.send([get_email(user, email, nonce.uuid.hex)])


def confirm_email_change(uuid: UUID, passwd: str) -> None:
    """Confirms the email change."""

    if (user := (nonce := EMailChangeNonce.use(uuid)).user).login(passwd):
        user.email = nonce.email
        user.save()
