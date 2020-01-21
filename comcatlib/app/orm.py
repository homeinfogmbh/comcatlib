"""Object-relational mappings."""

from peewee import CharField, DateTimeField, ForeignKeyField, TextField

from mdb import Customer
from peeweeplus import Argon2Field, EnumField, JSONModel, MySQLDatabase

from comcatlib.app.config import CONFIG
from comcatlib.app.enumerations import GrantType


DATABASE = MySQLDatabase.from_config(CONFIG['db'])


class ComcatModel(JSONModel):
    """A base model for the app backend."""

    class Meta:     # pylint: disable=C0115,R0903
        database = DATABASE
        schema = database.database


class User(ComcatModel):
    """An end user."""

    name = CharField()
    passwd = Argon2Field()
    customer = ForeignKeyField(Customer, column_name='customer')


class Client(ComcatModel):
    """A consumer id interested in accessing protected resources."""

    user = ForeignKeyField(User, column_name='user')
    grant_type = EnumField(GrantType)
    response_type = EnumField(GrantType)


class ClientScope(ComcatModel):
    """The list of scopes the client may request access to."""

    class Meta:     # pylint: disable=C0115,R0903
        table_name = 'client_scope'

    client = ForeignKeyField(Client, column_name='client', backref='scopes')
    scope = TextField()


class RedirectURI(ComcatModel):
    """These are the absolute URIs that a client
    may use to redirect to after authorization.
    """

    class Meta:     # pylint: disable=C0115,R0903
        table_name = 'redirect_uri'

    client = ForeignKeyField(
        Client, column_name='client', backref='redirect_uris')
    uri = TextField()


class BearerToken(ComcatModel):
    """The most common type of OAuth 2 token.
    Through the documentation this will be considered an object
    with several properties, such as token type and expiration date,
    and distinct from the access token it contains.
    Think of OAuth 2 tokens as containers and access tokens and
    refresh tokens as text.
    """

    class Meta:     # pylint: disable=C0115,R0903
        table_name = 'bearer_token'

    client = ForeignKeyField(
        Client, column_name='client', backref='bearer_tokens')
    user = ForeignKeyField(User, column_name='user', backref='bearer_tokens')
    access_token = CharField(100, unique=True)
    refresh_token = CharField(100, unique=True)
    expires_at = DateTimeField()


class BearerTokenScope(ComcatModel):
    """Scopes to which the token is bound. Attempt to access
    protected resources outside these scopes will be denied.
    """

    class Meta:     # pylint: disable=C0115,R0903
        table_name = 'bearer_token_scope'

    token = ForeignKeyField(BearerToken, column_name='token', backref='scopes')
    scope = TextField()


class PKCEChallenge(ComcatModel):
    """PKCE challenge."""

    class Meta:     # pylint: disable=C0115,R0903
        table_name = 'pkce_challenge'

    challenge = CharField(128)
    challenge_method = CharField(6)


class AuthorizationCode(ComcatModel):
    """This is specific to the Authorization Code grant and represent the
    temporary credential granted to the client upon successful authorization.
    It will later be exchanged for an access token, when that is done it should
    cease to exist. It should have a limited life time, less than ten minutes.
    This model is similar to the Bearer Token as it mainly acts a temporary
    storage of properties to later be transferred to the token.
    """

    class Meta:     # pylint: disable=C0115,R0903
        table_name = 'authorization_code'

    client = ForeignKeyField(
        Client, column_name='client', backref='authorization_codes')
    user = ForeignKeyField(
        User, column_name='user', backref='authorization_codes')
    code = CharField(100, unique=True)
    expires_at = DateTimeField()
    challenge = ForeignKeyField(
        PKCEChallenge, column_name='pkce_challenge', null=True)


class AuthorizationCodeScope(ComcatModel):
    """Scopes to which the token is bound. Attempt to access
    protected resources outside these scopes will be denied.
    """

    class Meta:     # pylint: disable=C0115,R0903
        table_name = 'authorization_code_scope'

    code = ForeignKeyField(
        AuthorizationCode, column_name='code', backref='scopes')
    scope = TextField()
