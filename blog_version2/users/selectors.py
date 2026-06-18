from django.db.models import QuerySet
from users.models import Profile, BaseUser

def get_profile(user:BaseUser) -> QuerySet[Profile]:
    return Profile.objects.get(user=user)
