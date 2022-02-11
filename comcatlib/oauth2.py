"""OAuth 2 framework."""

from oauth2gen import create_framework

from comcatlib.config import get_oauth2
from comcatlib.orm.user import User


__all__ = ['FRAMEWORK', 'REQUIRE_OAUTH', 'create_tables']


FRAMEWORK = create_framework(User, get_oauth2())
REQUIRE_OAUTH = FRAMEWORK.resource_protector


def create_tables():
    """Creates the tables for the ComCat database."""

    for model in FRAMEWORK.models:
        model.create_table()
