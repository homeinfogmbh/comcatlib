"""Tenant-to-tenant related functions."""

from peewee import JOIN, Expression, ModelCursorWrapper, ModelSelect

from tenant2tenant import TenantMessage, Visibility

from comcatlib.orm import DATABASE, User, UserTenantMessage


__all__ = [
    'select_tenant_messages',
    'get_tenant_messages',
    'get_deletable_tenant_messages',
    'get_deletable_tenant_message'
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
