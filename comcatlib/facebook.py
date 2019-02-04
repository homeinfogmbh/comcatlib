"""Facebook data aggregation."""

from cmslib.orm.charts import Facebook

from comcatlib.orm import Account
from comcatlib.presentation import Presentation
from comcatlib.urlproxy import encode_url


__all__ = ['get_posts']


def get_posts(account):
    """Yields posts for the respective account."""

    presentation = Presentation(Account[account.id])

    for chart in filter(Facebook.isinstance, presentation.charts):
        for account in chart.accounts:  # pylint: disable=R1704
            for post in account.posts:
                if post.image:
                    post.image = encode_url(post.image)
                else:
                    post.image = None

                yield post
