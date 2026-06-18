from django.db.models import QuerySet
from blog_version2.users.models import Profile, BaseUser

def get_profile(user:BaseUser) -> Profile:
    return Profile.objects.get(user=user)
