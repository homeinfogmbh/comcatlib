"""Damage report mappings."""

from peewee import BooleanField, ForeignKeyField

from damage_report import DamageReport

from comcatlib.orm.common import ComCatModel
from comcatlib.orm.files import File
from comcatlib.orm.user import User


__all__ = ['UserDamageReport']


class UserDamageReport(ComCatModel):
    """Maps a damage report to a ComCat account."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'user_damage_report'

    damage_report = ForeignKeyField(
        DamageReport, column_name='damage_report', on_delete='CASCADE')
    user = ForeignKeyField(User, column_name='user', on_delete='CASCADE')
    private = BooleanField(default=True)


class DamageReportAttachment(ComCatModel):
    """Maps an attachment onto a user damage report."""

    user_damage_report = ForeignKeyField(
        UserDamageReport, column_name='user_damage_report',
        on_delete='CASCADE')
    file = ForeignKeyField(File, column_name='file', on_delete='CASCADE')
