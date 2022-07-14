"""User content reporting."""

from typing import Optional

from marketplace import Offer
from tenantcalendar import UserEvent
from tenantforum import Response, Topic

from comcatlib.orm.reports import OfferReport
from comcatlib.orm.reports import TopicReport
from comcatlib.orm.reports import ResponseReport
from comcatlib.orm.reports import UserEventReport
from comcatlib.orm.user import User


__all__ = [
    'report_offer',
    'report_topic',
    'report_response',
    'report_user_event'
]


def report_offer(
        user: User,
        offer: Offer,
        *,
        title: Optional[bool] = None,
        text: Optional[bool] = None,
        image: Optional[bool] = None
) -> OfferReport:
    """Report an offer."""

    try:
        report = OfferReport.get(
            (OfferReport.user == user) & (OfferReport.offer == offer)
        )
    except OfferReport.DoesNotExist:
        report = OfferReport(user=user, offer=offer)

    return report.update(title=title, text=text, image=image)


def report_topic(
        user: User,
        topic: Topic,
        *,
        title: Optional[bool] = None,
        text: Optional[bool] = None,
        image: Optional[bool] = None
) -> TopicReport:
    """Report a tenant forum topic."""

    try:
        report = TopicReport.get(
            (TopicReport.user == user) & (TopicReport.topic == topic)
        )
    except TopicReport.DoesNotExist:
        report = TopicReport(user=user, topic=topic)

    return report.update(title=title, text=text, image=image)


def report_response(
        user: User,
        response: Response,
        *,
        title: Optional[bool] = None,
        text: Optional[bool] = None,
        image: Optional[bool] = None
) -> ResponseReport:
    """Report a tenant forum response."""

    try:
        report = ResponseReport.get(
            (ResponseReport.user == user)
            & (ResponseReport.response == response)
        )
    except ResponseReport.DoesNotExist:
        report = ResponseReport(user=user, response=response)

    return report.update(title=title, text=text, image=image)


def report_user_event(
        user: User,
        event: UserEvent,
        *,
        title: Optional[bool] = None,
        text: Optional[bool] = None,
        image: Optional[bool] = None
) -> UserEventReport:
    """Report a tenant forum response."""

    try:
        report = UserEventReport.get(
            (UserEventReport.user == user) & (UserEventReport.event == event)
        )
    except UserEventReport.DoesNotExist:
        report = UserEventReport(user=user, event=event)

    return report.update(title=title, text=text, image=image)
