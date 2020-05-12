"""ComCat menu tagging."""

from enum import Enum

from peewee import ForeignKeyField

from cmslib.orm.charts import BaseChart
from peeweeplus import EnumField

from comcatlib.orm.common import ComCatModel


__all__ = ['Menu', 'BaseChartMenu']


class Menu(Enum):
    """Available menus."""

    IMPRINT = 'imprint'
    EMERGENCY = 'emergency'
    HOUSE_INFO = 'house info'
    NEWS = 'news'


class BaseChartMenu(ComCatModel):
    """Many-to-many mapping of charts an menus."""

    class Meta:     # pylint: disable=C0115,R0903
        table_name = 'base_chart_menu'

    base_chart = ForeignKeyField(
        BaseChart, column_name='base_chart', on_delete='CASCADE')
    menu = EnumField(Menu)

    @classmethod
    def add(cls, base_chart, menu):
        """Creates a new record from a JSON-ish dict."""
        condition = cls.base_chart == base_chart
        condition &= cls.menu == menu

        try:
            return cls.get(condition)
        except cls.DoesNotExist:
            return cls(base_chart=base_chart, menu=menu)
