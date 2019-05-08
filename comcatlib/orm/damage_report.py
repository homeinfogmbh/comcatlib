"""Damage report mappings."""

from peewee import ForeignKeyField

from damage_report import DamageReport

from comcatlib.api import Account, ComCatModel


__all__ = ['AccountDamageReport']


class AccountDamageReport(ComCatModel):
    """Maps a damage report to a ComCat account."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'account_damage_report'

    account = ForeignKeyField(
        Account, column_name='account', on_delete='CASCADE')
    damage_report = ForeignKeyField(
        DamageReport, column_name='damage_report', on_delete='CASCADE')
