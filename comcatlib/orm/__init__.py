"""Object relational mappings."""


from comcatlib.orm.address import Address
from comcatlib.orm.common import DATABASE, ComCatModel
from comcatlib.orm.content import UserBaseChart
from comcatlib.orm.content import UserConfiguration
from comcatlib.orm.content import UserMenu
from comcatlib.orm.damage_report import UserDamageReport
from comcatlib.orm.group import GroupMemberUser
from comcatlib.orm.session import Session
from comcatlib.orm.tenement import Tenement
from comcatlib.orm.user import get_user, User


__all__ = [
    'DATABASE',
    'MODELS',
    'get_user',
    'User',
    'Address',
    'UserBaseChart',
    'UserConfiguration',
    'UserMenu',
    'UserDamageReport',
    'ComCatModel',
    'GroupMemberUser',
    'Session',
    'Tenement'
]


# Order matters here.
MODELS = (
    Address,
    Tenement,
    User,
    Session,
    UserBaseChart,
    UserConfiguration,
    UserMenu,
    UserDamageReport,
    GroupMemberUser
)
