"""Facebook data aggregation."""

from functools import partial

from cmslib.orm.charts import Facebook

from comcatlib.orm import Account
from comcatlib.presentation import Presentation
from comcatlib.urlproxy import encode_url


__all__ = ['get_accounts', 'get_posts']


def get_accounts(account):
    """Yields facebook accounts."""

    presentation = Presentation(Account[account.id])

    for chart in filter(partial(isinstance, Facebook), presentation.charts):
        for facebook_account in chart.accounts:
            yield facebook_account


def get_posts(facebook_account):
    """Yields posts for the respective facebook account."""

    for post in facebook_account.posts:
        if post.image:
            post.image = encode_url(post.image)
        else:
            post.image = None

        yield post
