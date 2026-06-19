from django.db.models import QuerySet
from blog_version2.users.models import BaseUser
from blog_version2.home.models import Subscription



def get_subscribers(*, user:BaseUser) -> QuerySet[Subscription]:
    return Subscription.objects.filter(subscriber=user)