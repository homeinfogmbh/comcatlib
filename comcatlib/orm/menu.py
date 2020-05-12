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

    base_chart = ForeignKeyField(
        BaseChart, column_name='base_chart', on_delete='CASCADE')
    menu = EnumField(Menu)
