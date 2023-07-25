"""Tenant calendar management."""

from datetime import timedelta
from random import randint

from mdb import Customer, Tenement
from tenantcalendar import UserEvent

from comcatlib.demo.common import LOGGER, rand_date_in_month, randzipfill
from comcatlib.orm.user import User


__all__ = ["create_events", "delete_events"]


def create_events(users: list[User], events: list[dict[str, str]]) -> None:
    """Adds the given events."""

    for user, event in randzipfill(users, events):
        add_user_event(user, event)


def delete_events(customer: Customer) -> None:
    """Deletes the user events of the given customer."""

    for user_event in (
        UserEvent.select()
        .join(User)
        .join(Tenement)
        .where(Tenement.customer == customer)
    ):
        user_event.delete_instance()


def add_user_event(user: User, event: dict[str, str]) -> None:
    """Adds the respective user event."""

    LOGGER.info("Creating user event: %s", title := event["title"])
    user_event = UserEvent(
        title=title,
        text=event["text"],
        start=(start := rand_date_in_month()),
        end=start + timedelta(hours=randint(1, 24)),
        created=start - timedelta(days=randint(1, 60)),
        user=user,
        email=user.email,
    )
    user_event.save()
