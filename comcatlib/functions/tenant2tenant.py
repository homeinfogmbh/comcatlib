"""Tenant-to-tenant related functions."""

from datetime import datetime
from typing import Optional

from peewee import JOIN, Expression, ModelCursorWrapper, ModelSelect

from tenant2tenant import Configuration, TenantMessage, Visibility

from comcatlib.orm import DATABASE, User, UserTenantMessage


__all__ = [
    'add_user_tenant_message',
    'get_deletable_tenant_message',
    'get_deletable_tenant_messages',
    'get_tenant_messages',
    'jsonify_tenant_message',
    'select_tenant_messages'
]


def get_condition(user: User) -> Expression:
    """Returns a select condition of tenant messages for unprivileged users."""

    return (
        # Always allow own messages.
        (UserTenantMessage.user == user)
        | (
            # Show messages of the same customer
            # under the following conditions.
            (TenantMessage.customer == user.tenement.customer)
            # Only show released messages.
            & (TenantMessage.released == 1)
            & (
                (
                    # If the visibility is set to customer-wide,
                    # show all those entries of the same customer.
                    TenantMessage.visibility == Visibility.CUSTOMER
                ) | (
                    # If the visibility is restricted to tenement, only
                    # show entries of the same address.
                    (TenantMessage.visibility == Visibility.TENEMENT)
                    & (TenantMessage.address == user.tenement.address)
                )
            )
        )
    )


def select_tenant_messages(user: User) -> ModelSelect:
    """Yields the tenant-to-tenant messages the current user may access."""

    select = TenantMessage.select(
        UserTenantMessage, User, cascade=True).join_from(
        TenantMessage, UserTenantMessage, JOIN.LEFT_OUTER).join(
        User, JOIN.LEFT_OUTER)

    if user.admin:
        # Admins can see all tenant-to-tenant messages of their company.
        return select.where(TenantMessage.customer == user.tenement.customer)

    return select.where(get_condition(user))


def get_tenant_messages(user: User) -> ModelCursorWrapper:
    """Yields messages."""

    return select_tenant_messages(user).execute(DATABASE)


def get_deletable_tenant_messages(user: User) -> ModelSelect:
    """Returns a tenant-to-tenant message
    that the current user may delete.
    """

    select = TenantMessage.select()
    condition = TenantMessage.customer == user.tenement.customer

    if not user.admin:
        select = TenantMessage.select().join(UserTenantMessage)
        condition &= UserTenantMessage.user == user

    return select.where(condition)


def get_deletable_tenant_message(user: User, ident: int) -> ModelSelect:
    """Returns a tenant-to-tenant message
    that the current user may delete.
    """

    return get_deletable_tenant_messages(user).where(
        TenantMessage.id == ident).get()


def add_user_tenant_message(json: dict, user: User) -> UserTenantMessage:
    """Adds a tenant message."""

    message = json['message']
    tenant_message = TenantMessage.add(
        user.tenement.customer, user.tenement.address, message)
    tenant_message.subject = json.get('subject')
    visibility = json.get('visibility')

    if visibility:
        tenant_message.visibility = Visibility(visibility)
    else:
        tenant_message.visibility = Visibility.TENEMENT

    configuration = Configuration.for_customer(user.tenement.customer)

    if configuration.auto_release:
        tenant_message.released = True
        tenant_message.start_date = now = datetime.now()
        tenant_message.end_date = now + configuration.release_time

    tenant_message.save()
    user_tenant_message = UserTenantMessage(
        tenant_message=tenant_message, user=user)
    user_tenant_message.save()
    return user_tenant_message


def is_own_message(user: User, message: TenantMessage) -> bool:
    """Determines whether the tenant message is of the current user."""

    try:
        return message.usertenantmessage.user_id == user.id
    except AttributeError:
        return False


def get_sender_name(message: TenantMessage) -> Optional[str]:
    """Returns the sender name if available."""

    try:
        return message.usertenantmessage.user.name
    except AttributeError:
        return None


def jsonify_tenant_message(user: User, message: TenantMessage,
                           *args, **kwargs) -> dict:
    """Converts a tenant message into a JSON-ish dict."""

    json = message.to_json(*args, **kwargs)
    json['own'] = is_own_message(user, message)
    json['sender'] = get_sender_name(message)
    return json
