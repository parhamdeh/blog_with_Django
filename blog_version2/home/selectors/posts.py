from django.db.models import QuerySet
from blog_version2.users.models import BaseUser
from blog_version2.home.models import Posts, Subscription
from blog_version2.home.filters import PostFilter



def post_detail(*, slug:str, user:BaseUser, self_include:bool = True) -> QuerySet[Posts]:
    subscription = list(Subscription.objects.filter(subscriber=user).values_list("target", flat=True))
     # Include current user's own posts if requested
    if self_include:
        subscription.append(user.id)
    # Return a post by slug only if its author is in the allowed list
    return Posts.objects.get(slug=slug, author__in=subscription)

def post_list(*, filters=None, user:BaseUser, self_include:bool = True) -> QuerySet[Posts]:
    filters = filters or {}
    subscription = list(Subscription.objects.filter(subscriber=user).values_list("target", flat=True))

    if self_include:
        subscription.append(user.id)

    # Return filtered posts from followed users (and optionally self)
    if subscription:
        qs = Posts.objects.filter(author__in=subscription)
        return PostFilter(filters, qs).qs
    
    return Posts.objects.none()
