"""Content assigned to ComCat accounts."""

from peewee import ForeignKeyField, IntegerField

from comcatlib.orm.common import ComCatModel
from comcatlib.orm.user import User

from cmslib.orm.charts import ChartMode, BaseChart
from cmslib.orm.configuration import Configuration
from cmslib.orm.menu import Menu
from cmslib.orm.user import get_user


__all__ = ['UserBaseChart', 'UserConfiguration', 'UserMenu']


def get_base_chart(ident)::
    """Returns the respective base chart."""

    try:
        return BaseChart.get(
            (BaseChart.id == ident) & (BaseChart.customer == customer))
    except BaseChart.DoesNotExist:
        raise NoSuchBaseChart()


class UserContent(ComCatModel):
    """Common abstract content mapping."""

    user = ForeignKeyField(User, column_name='user', on_delete='CASCADE')


class UserBaseChart(UserContent):
    """Association of a base chart with a user."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'user_base_chart'

    base_chart = ForeignKeyField(
        BaseChart, column_name='base_chart', on_delete='CASCADE')
    index = IntegerField(default=0)

    @classmethod
    def from_json(cls, json, **kwargs):
        """Creates a new group base chart."""
        user = json.pop('user')
        base_chart = json.pop('base_chart')
        record = super().from_json(json, **kwargs)
        base_chart = get_base_chart(base_chart)
        record.user = get_user(user)
        record.base_chart = base_chart
        return record

    @property
    def chart(self):
        """Returns the respective chart."""
        return self.base_chart.chart

    def to_json(self):
        """Returns a JSON-ish dict."""
        return {
            'id': self.id,
            'chart': self.chart.to_json(mode=ChartMode.BRIEF),
            'index': self.index
        }


class UserConfiguration(UserContent):
    """Association of a configuration with a user."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'user_configuration'

    configuration = ForeignKeyField(
        Configuration, column_name='configuration', on_delete='CASCADE')

    def to_json(self):
        """Returns a JSON-ish dict."""
        return {'id': self.id, 'configuration': self.configuration_id}


class UserMenu(UserContent):
    """Association of a menu with a user."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'user_menu'

    menu = ForeignKeyField(Menu, column_name='menu', on_delete='CASCADE')

    def to_json(self):
        """Returns a JSON-ish dict."""
        return {'id': self.id, 'menu': self.menu_id}
