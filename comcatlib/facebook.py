"""Facebook data aggregation."""

from functools import partial

from cmslib.orm.charts import Facebook

from comcatlib.api import Account
from comcatlib.presentation import Presentation
from comcatlib.urlproxy import encode_url


__all__ = ['get_accounts', 'get_posts']


def get_accounts(comcat_account):
    """Yields facebook accounts."""

    presentation = Presentation(Account[comcat_account.id])

    for chart in filter(partial(isinstance, Facebook), presentation.charts):
        for account in chart.accounts:
            yield account


def get_posts(account):
    """Yields posts for the respective facebook account."""

    for post in account.posts:
        if post.image:
            post.image = encode_url(post.image)
        else:
            post.image = None

        yield post
