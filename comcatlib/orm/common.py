"""Common ORM stuff."""

from peeweeplus import MySQLDatabaseProxy, JSONModel

from comcatlib.config import CONFIG_FILE


__all__ = ['DATABASE', 'ComCatModel']


DATABASE = MySQLDatabaseProxy('comcat', CONFIG_FILE)


class ComCatModel(JSONModel):
    """Basic ConCat model."""

    class Meta:
        database = DATABASE
        schema = database.database
