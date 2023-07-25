"""ComCat menu tagging."""

from __future__ import annotations
from enum import Enum
from typing import Union

from peewee import ForeignKeyField, Select

from cmslib import BaseChart
from mdb import Company, Customer
from peeweeplus import EnumField

from comcatlib.orm.common import ComCatModel


__all__ = ["Menu", "MenuBaseChart"]


class Menu(Enum):
    """Available menus."""

    DATA_PROTECTION = "data protection"
    IMPRINT = "imprint"
    CONTACT = "contact"
    DAMAGES = "damages"
    DOCUMENTS = "documents"
    SERVICE_NUMBERS = "service numbers"
    NEWS = "news"


class MenuBaseChart(ComCatModel):
    """Many-to-many mapping of charts and menus."""

    class Meta:
        table_name = "base_chart_menu"

    base_chart = ForeignKeyField(
        BaseChart, column_name="base_chart", on_delete="CASCADE", lazy_load=False
    )
    menu = EnumField(Menu)

    @classmethod
    def add(cls, base_chart: Union[BaseChart, int], menu: Menu) -> MenuBaseChart:
        """Creates a new record from a JSON-ish dict."""
        condition = cls.base_chart == base_chart
        condition &= cls.menu == menu

        try:
            return cls.select(cascade=True).where(condition).get()
        except cls.DoesNotExist:
            record = cls(base_chart=base_chart, menu=menu)
            record.save()
            return record

    @classmethod
    def select(cls, *args, cascade: bool = False) -> Select:
        """Selects base chart menus."""
        if not cascade:
            return super().select(*args)

        return (
            super()
            .select(*{cls, BaseChart, Customer, Company, *args})
            .join(BaseChart)
            .join(Customer)
            .join(Company)
        )
