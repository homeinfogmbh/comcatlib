"""Damage report mappings."""

from peewee import ForeignKeyField

from damage_report import DamageReport

from comcatlib.orm.common import ComCatModel
from comcatlib.orm.user import User


__all__ = ['UserDamageReport']


class UserDamageReport(ComCatModel):    # pylint: disable=R0903
    """Maps a damage report to a ComCat account."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'user_damage_report'

    damage_report = ForeignKeyField(
        DamageReport, column_name='damage_report', on_delete='CASCADE')
    user = ForeignKeyField(User, column_name='user', on_delete='CASCADE')
