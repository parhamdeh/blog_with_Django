from blog_version2.users.models import BaseUser
from blog_version2.home.models import Posts, Subscription
from blog_version2.home.filters import PostFilter

from django.db.models import QuerySet
from django.db.models import Q



def post_detail(*, slug: str, user: BaseUser, self_include: bool = True) -> Posts:
    subscription = Subscription.objects.filter(
        subscriber=user
    ).values_list("target", flat=True)

    if self_include:
        subscription.append(user.id)
    # Public posts are visible to everyone.
    # Private posts are visible only to followers.
    filters = (
        Q(author__is_private=False) |
        Q(author__in=subscription)
    )

    return Posts.objects.get(filters, slug=slug)

def post_list(*, filters=None, user: BaseUser, self_include: bool = True) -> QuerySet[Posts]:
    filters = filters or {}

    subscription = Subscription.objects.filter(
        subscriber=user
    ).values_list("target", flat=True)
    
    # Public authors are always visible.
    # Private authors require an active subscription.
    visibility_filter = (
        Q(author__is_private=False) |
        Q(author__in=subscription)
    )

    if self_include:
        visibility_filter |= Q(author=user)

    qs = Posts.objects.filter(visibility_filter)

    return PostFilter(filters, qs).qs