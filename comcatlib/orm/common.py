"""Common ORM stuff."""

from peeweeplus import MySQLDatabaseProxy, JSONModel

from comcatlib.config import CONFIG_FILE


__all__ = ['DATABASE', 'ComCatModel']


DATABASE = MySQLDatabaseProxy('comcat', CONFIG_FILE)


class ComCatModel(JSONModel):   # pylint: disable=R0903
    """Basic comcat model."""

    class Meta:     # pylint: disable=C0111,R0903
        database = DATABASE
        schema = database.database
