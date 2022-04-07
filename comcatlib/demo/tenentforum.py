"""Demo tenant forum entry management."""

from datetime import datetime, timedelta
from random import shuffle
from typing import Iterable

from mdb import Customer, Tenement
from tenantforum import Topic, Response

from comcatlib.demo.common import randdate
from comcatlib.orm.user import User


__all__ = ['create_topics', 'delete_topics']


def create_topic(user: User, title: str, text: str, offset: int) -> Topic:
    """Creates a dummy topic."""

    timestamp = randdate(
        datetime.now() - timedelta(days=offset),
        datetime.now()
    )
    topic = Topic(user=user, title=title, text=text, created=timestamp)
    topic.save()
    return topic


def create_response(user: User, topic: Topic, text: str, index: int) -> None:
    """Creates a response to a topic."""

    timestamp = randdate(
        topic.created,
        topic.created + timedelta(hours=index + 1, minutes=index + 1)
    )
    response = Response(user=user, topic=topic, text=text, created=timestamp)
    response.save()


def create_topics(users: Iterable[User], threads: Iterable[dict]) -> None:
    """Creates the respective topics."""

    thread_creators = list(users)
    shuffle(thread_creators)

    for topic_index, (op, thread) in enumerate(zip(thread_creators, threads)):
        topic = create_topic(
            op,
            thread['topic']['title'],
            thread['topic']['text'],
            len(thread_creators) - topic_index
        )
        responders = list(users)
        shuffle(responders)

        for response_index, (responder, response) in enumerate(zip(
                responders, thread['responses']
        )):
            create_response(responder, topic, response, response_index)


def delete_topics(customer: Customer) -> None:
    """Deletes topics of the given customer."""

    for topic in Topic.select().join(User).join(Tenement).where(
        Tenement.customer == customer
    ):
        topic.delete_instance()
