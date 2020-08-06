"""Damage report mappings."""

from peewee import ForeignKeyField

from damage_report import DamageReport

from comcatlib.orm.common import ComCatModel
from comcatlib.orm.files import File
from comcatlib.orm.user import User


__all__ = ['UserDamageReport', 'DamageReportAttachment']


class UserDamageReport(ComCatModel):    # pylint: disable=R0903
    """Maps a damage report to a ComCat account."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'user_damage_report'

    damage_report = ForeignKeyField(
        DamageReport, column_name='damage_report', on_delete='CASCADE')
    user = ForeignKeyField(User, column_name='user', on_delete='CASCADE')


class DamageReportAttachment(ComCatModel):  # pylint: disable=R0903
    """Maps an attachment onto a user damage report."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'damage_report_attachment'

    user_damage_report = ForeignKeyField(
        UserDamageReport, column_name='user_damage_report',
        on_delete='CASCADE')
    file = ForeignKeyField(File, column_name='file', on_delete='CASCADE')
