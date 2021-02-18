"""Customer-specific settings."""

from peewee import IntegerField

from comcatlib.orm.common import ComCatModel


__all__ = ['Settings']


USER_QUOTA = 10


class Settings(ComCatModel):
    """Customer-specific settings model."""

    user_quota = IntegerField(default=USER_QUOTA)
