"""Client registration."""

from flask import request

from wsgilib import JSON

from comcatlib.messages import INVALID_TOKEN, NO_TOKEN_SPECIFIED
from comcatlib.orm import Client, ClientRegistrationToken


__all__ = ['register_client']


def register_client():
    """Registers a client."""

    token = request.args.get('registration_token')

    if not token:
        return NO_TOKEN_SPECIFIED

    try:
        token = ClientRegistrationToken.get(
            ClientRegistrationToken.token == token)
    except ClientRegistrationToken.DoesNotExist:
        return INVALID_TOKEN

    if token.valid:
        return INVALID_TOKEN

    token.used = True
    token.save()
    transaction, secret = Client.from_json(request.json)
    transaction.save()
    json = transaction.primary.to_json()
    json['clientSecret'] = secret
    return JSON(json)
