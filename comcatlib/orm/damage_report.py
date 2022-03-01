"""Damage report mappings."""

from peewee import ForeignKeyField, Select

from damage_report import DamageReport
from mdb import Address, Company, Customer, Tenement

from comcatlib.orm.common import ComCatModel
from comcatlib.orm.user import User


__all__ = ['UserDamageReport']


class UserDamageReport(ComCatModel):
    """Maps a damage report to a ComCat account."""

    class Meta:
        table_name = 'user_damage_report'

    damage_report = ForeignKeyField(
        DamageReport, column_name='damage_report', on_delete='CASCADE',
        lazy_load=False
    )
    user = ForeignKeyField(
        User, column_name='user', on_delete='CASCADE', lazy_load=False
    )

    @classmethod
    def select(cls, *args, cascade: bool = False) -> Select:
        """Selects user damage reports."""
        if not cascade:
            return super().select(*args)

        return super().select(*{
            cls, DamageReport, User, Tenement, Customer, Company, Address,
            *args
        }).join(DamageReport).join_from(cls, User).join(Tenement).join(
            Customer).join(Company).join_from(Tenement, Address)
