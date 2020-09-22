"""Client registration."""

from flask import request

from wsgilib import JSON

from comcatlib.app.login import get_current_user
from comcatlib.messages import INVALID_TOKEN
from comcatlib.messages import NO_TOKEN_SPECIFIED
from comcatlib.messages import NO_USER_SPECIFIED
from comcatlib.orm import Client, ClientRegistrationToken


__all__ = ['register_client']


def register_client():
    """Registers a client."""

    user = get_current_user()

    if user is None:
        return NO_USER_SPECIFIED

    token = request.args.get('registration_token')
    print('[DEBUG] TOKEN:', token, flush=True)

    if not token:
        return NO_TOKEN_SPECIFIED

    try:
        token = ClientRegistrationToken.get(
            ClientRegistrationToken.token == token)
    except ClientRegistrationToken.DoesNotExist:
        return INVALID_TOKEN

    if not token.valid:
        return INVALID_TOKEN

    token.used = True
    token.save()
    transaction, secret = Client.from_json(request.json, user)
    transaction.save()
    json = transaction.primary.to_json()
    json['clientSecret'] = secret
    return JSON(json)
