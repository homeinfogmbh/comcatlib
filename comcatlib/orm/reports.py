"""Reports of inappropriate user content."""

from __future__ import annotations
from typing import Any, Iterator, Optional

from peewee import BooleanField, ForeignKeyField

from marketplace import Offer
from tenantcalendar import UserEvent
from tenantforum import Response, Topic

from comcatlib.orm.common import ComCatModel
from comcatlib.orm.user import User


__all__ = ['OfferReport', 'TopicReport', 'ResponseReport', 'UserEventReport']


class Report(ComCatModel):
    """Common report basis."""

    reporter = ForeignKeyField(User, column_name='user', on_delete='CASCADE')
    title = BooleanField(default=False)
    text = BooleanField(default=False)
    image = BooleanField(default=False)

    @property
    def options(self) -> Iterator[bool]:
        """Yields all set options."""
        yield self.title
        yield self.text
        yield self.image

    @property
    def other(self) -> bool:
        """Return whether none specific option was selected."""
        return not any(self.options)

    def update(
            self,
            title: Optional[bool] = None,
            text: Optional[bool] = None,
            image: Optional[bool] = None
    ) -> Report:
        """Updates the report and returns it."""
        if title is not None:
            self.title = title

        if text is not None:
            self.text = text

        if image is not None:
            self.image = image

        self.save()
        return self

    def to_json(self, *, other: bool = True, **kwargs) -> dict[str, Any]:
        """Return a JSON-ish dict."""
        json = super().to_json(**kwargs)

        if other:
            json['other'] = self.other

        return json


class OfferReport(Report):
    """Report for a marketplace offer."""

    class Meta:
        table_name = 'offer_report'

    offer = ForeignKeyField(Offer, column_name='offer', on_delete='CASCADE')


class TopicReport(Report):
    """Report for a tenant forum topic."""

    class Meta:
        table_name = 'topic_report'

    topic = ForeignKeyField(Topic, column_name='topic', on_delete='CASCADE')


class ResponseReport(Report):
    """Report for a tenant forum response."""

    class Meta:
        table_name = 'response_report'

    response = ForeignKeyField(
        Response, column_name='response', on_delete='CASCADE'
    )


class UserEventReport(Report):
    """Report for a user event."""

    class Meta:
        table_name = 'user_event_report'

    event = ForeignKeyField(
        UserEvent, column_name='user_event', on_delete='CASCADE'
    )
