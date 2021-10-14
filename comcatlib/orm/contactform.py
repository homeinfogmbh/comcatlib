"""Contact form related ORM models."""

from notificationlib import get_email_orm_model

from comcatlib.orm.common import ComCatModel


__all__ = ['ContactEmails']


ContactEmails = get_email_orm_model(ComCatModel, table_name='contact_emails')
