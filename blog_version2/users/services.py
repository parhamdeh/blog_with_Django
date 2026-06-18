from .models import Profile, BaseUser

from django.db.models import QuerySet
from django.db import transaction



def create_profile(*, user:BaseUser, bio:str | None) -> QuerySet[Profile]:
    return Profile.objects.create(user=user, bio=bio)
    

def create_user(*, username:str, email:str, password:str) -> QuerySet[BaseUser]:
    return BaseUser.objects.create_user(username=username, email=email, password=password)

@transaction.atomic
def register(*, bio:str, username:str, email:str, password:str) -> QuerySet[BaseUser]:
    user = create_user(username=username, email=email, password=password)
    create_profile(user=user, bio=bio)

    return user