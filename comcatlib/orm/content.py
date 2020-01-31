"""Content assigned to ComCat accounts."""

from peewee import ForeignKeyField, IntegerField

from comcatlib.orm.common import ComCatModel
from comcatlib.orm.user import User

from cmslib.orm.charts import ChartMode, BaseChart
from cmslib.orm.configuration import Configuration
from cmslib.orm.menu import Menu


__all__ = ['AccountBaseChart', 'AccountConfiguration', 'AccountMenu']


class UserContent(ComCatModel):
    """Common abstract content mapping."""

    user = ForeignKeyField(User, column_name='user', on_delete='CASCADE')


class AccountBaseChart(UserContent):
    """Association of a base chart with a user."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'user_base_chart'

    base_chart = ForeignKeyField(
        BaseChart, column_name='base_chart', on_delete='CASCADE')
    index = IntegerField(default=0)

    @classmethod
    def from_json(cls, json, **kwargs):
        """Creates a new group base chart."""
        base_chart = json.pop('base_chart')
        index = json.pop('index', 0)
        record = super().from_json(json, **kwargs)
        base_chart = get_base_chart(base_chart)
        record.account = account
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


class AccountConfiguration(UserContent):
    """Association of a configuration with an account."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'user_configuration'

    configuration = ForeignKeyField(
        Configuration, column_name='configuration', on_delete='CASCADE')

    def to_json(self):
        """Returns a JSON-ish dict."""
        return {'id': self.id, 'configuration': self.configuration_id}


class AccountMenu(UserContent):
    """Association of a menu with an account."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'user_menu'

    menu = ForeignKeyField(Menu, column_name='menu', on_delete='CASCADE')

    def to_json(self):
        """Returns a JSON-ish dict."""
        return {'id': self.id, 'menu': self.menu_id}
