"""Demo tenant forum entry management."""

from datetime import datetime, timedelta
from typing import Sequence

from mdb import Customer, Tenement
from tenantforum import Topic, Response

from comcatlib.demo.common import LOGGER, randdate, randzipfill
from comcatlib.orm.user import User


__all__ = ['create_topics', 'delete_topics']


def create_topics(users: Sequence[User], threads: Sequence[dict]) -> None:
    """Creates the respective topics."""

    for topic_index, (op, thread) in enumerate(
            randzipfill(users, threads)
    ):
        topic = create_topic(
            op,
            thread['title'],
            thread['text'],
            len(threads) - topic_index
        )

        for response_index, (responder, response) in enumerate(
                randzipfill(users, thread['responses'])
        ):
            create_response(responder, topic, response, response_index)


def delete_topics(customer: Customer) -> None:
    """Deletes topics of the given customer."""

    for topic in Topic.select().join(User).join(Tenement).where(
        Tenement.customer == customer
    ):
        LOGGER.info('Deleting topic "%s"', topic.title)
        topic.delete_instance()


def create_topic(user: User, title: str, text: str, offset: int) -> Topic:
    """Creates a dummy topic."""

    LOGGER.info('Creating topic: "%s" by user %s', title, user.email)
    timestamp = randdate(
        datetime.now() - timedelta(days=offset),
        datetime.now()
    )
    topic = Topic(user=user, title=title, text=text, created=timestamp)
    topic.save()
    return topic


def create_response(user: User, topic: Topic, text: str, index: int) -> None:
    """Creates a response to a topic."""

    LOGGER.info('Creating response by user %s', user.email)
    timestamp = randdate(
        topic.created,
        topic.created + timedelta(hours=index + 1, minutes=index + 1)
    )
    response = Response(user=user, topic=topic, text=text, created=timestamp)
    response.save()
