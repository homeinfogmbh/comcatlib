"""Common ORM stuff."""

from peeweeplus import MySQLDatabase, JSONModel

from comcatlib.config import CONFIG


__all__ = ['DATABASE', 'ComCatModel']


DATABASE = MySQLDatabase.from_config(CONFIG['db'])


class ComCatModel(JSONModel):
    """Basic comcat model."""

    class Meta:     # pylint: disable=C0111,R0903
        database = DATABASE
        schema = database.database
