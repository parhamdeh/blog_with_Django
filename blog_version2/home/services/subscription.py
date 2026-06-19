from blog_version2.home.models import Subscription
from blog_version2.users.models import BaseUser

from django.db.models import QuerySet
from django.db import transaction
from django.utils.text import slugify



def count_follower(*, user:BaseUser) -> int:
    return Subscription.objects.filter(target=user).count()

def count_following(*, user:BaseUser) -> int:
    return Subscription.objects.filter(subscriber=user).count()

def subscribe(*, user:BaseUser, username:str) -> QuerySet[Subscription]:
    target = BaseUser.objects.get(username=username)
    sub = Subscription(subscriber=user, target=target)
    sub.full_clean()
    sub.save()
    return sub

def unsubscribe(*, user:BaseUser, username:str) -> dict:
    target = BaseUser.objects.get(username=username)
    Subscription.objects.get(subscriber=user, target=target).delete()