"""Facebook data aggregation."""

from cmslib.orm.charts import FacebookChart, FacebookAccount
from cmslib.presentation.comcat_account import Presentation

from comcatlib.orm import Account
from comcatlib.urlproxy import encode_url


__all__ = ['get_posts']


def get_posts(account):
    """Yields posts for the respective account."""

    presentation = Presentation(Account[account.id])

    for chart in presentation.charts:
        if isinstance(chart, FacebookChart):
            for facebook_account in FacebookAccount.select().where(
                    FacebookAccount.chart == chart):
                for post in facebook_account.posts:
                    if post.image:
                        post.image = encode_url(post.image)
                    else:
                        post.image = None

                    yield post
