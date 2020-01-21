"""OAuth 2.0 request validator."""

from oauthlib.oauth2 import RequestValidator as _RequestValidator

from comcatlib.app.orm import Client


class RequestValidator(_RequestValidator):
    """Validates requests."""

    def validate_client_id(self, client_id, request):
        """Validates a client ID."""
        try:
            Client.get(Client.id == client_id)
        except Client.DoesNotExist:
            return False

        return True
