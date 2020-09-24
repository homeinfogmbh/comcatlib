"""Client registration."""

from uuid import UUID

from flask import request

from wsgilib import JSON

from comcatlib.exceptions import NonceUsed
from comcatlib.messages import INVALID_UUID
from comcatlib.messages import INVALID_NONCE
from comcatlib.messages import MISSING_NONCE
from comcatlib.orm import Client, InitializationNonce


__all__ = ['register_client']


def register_client():
    """Registers a client."""

    nonce = request.json.pop('nonce', None)

    if nonce is None:
        return MISSING_NONCE

    try:
        uuid = UUID(nonce)
    except ValueError:
        return INVALID_UUID

    try:
        user = InitializationNonce.use(uuid)
    except NonceUsed:
        return INVALID_NONCE

    transaction, secret = Client.add(request.json, user)
    transaction.save()
    json = transaction.primary.to_json()
    json['clientSecret'] = secret
    return JSON(json)
