"""Contact form mailing."""

from typing import Iterator
from xml.etree.ElementTree import Element, SubElement, tostring

from emaillib import EMail
from mdb import Customer

from comcatlib.email import SENDER, get_mailer
from comcatlib.orm.contactform import ContactEmails
from comcatlib.orm.user import User


__all__ = ['send_contact_mails']


def get_html_body(user: User, json: dict) -> Element:   # pylint: disable=R0914
    """Returns a HTML element."""

    html = Element('html')
    header = SubElement(html, 'header')
    SubElement(header, 'meta', attrib={'charset': 'UTF-8'})
    body = SubElement(html, 'body')
    h1 = SubElement(body, 'h1')     # pylint: disable=C0103
    h1.text = 'Kontaktanfrage'
    h2 = SubElement(body, 'h2')     # pylint: disable=C0103
    h2.text = 'Benutzerdaten'
    table = SubElement(body, 'table')
    table_header = SubElement(table, 'tr')
    h_account = SubElement(table_header, 'th')
    h_account.text = 'Benutzerkonto'
    h_email = SubElement(table_header, 'th')
    h_email.text = 'E-Mail-Adresse'
    h_phone = SubElement(table_header, 'th')
    h_phone.text = 'Telefonnummer'
    row1 = SubElement(table, 'tr')
    col_account = SubElement(row1, 'th')
    col_account.text = str(user.id)
    col_email = SubElement(row1, 'th')
    col_email.text = json['email']
    col_phone = SubElement(row1, 'th')
    col_phone.text = json['phone']
    h2 = SubElement(body, 'h2')     # pylint: disable=C0103
    h2.text = 'Nachricht'
    msg = SubElement(body, 'p')
    msg.text = json['message']
    return html


def get_recipients(customer: Customer) -> Iterator[str]:
    """Yields email addresses for the customer."""

    for contact_email in ContactEmails.select().where(
            ContactEmails.customer == customer):
        yield contact_email.email


def get_contact_emails(user: User, json: dict) -> Iterator[EMail]:
    """Creates a contact email."""

    html = tostring(get_html_body(user, json))

    for recipient in get_recipients(user.tenement.customer):
        email = EMail('Neue Kontaktanfrage', SENDER, recipient, html=html)
        email['Reply-To'] = json['email']
        yield email


def send_contact_mails(user: User, json: dict) -> bool:
    """Sends contact emails."""

    return get_mailer().send(get_contact_emails(user, json))
