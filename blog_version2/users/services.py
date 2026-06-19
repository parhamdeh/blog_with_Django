from blog_version2.users.models import Profile, BaseUser

from django.db import transaction



def create_profile(*, user:BaseUser, bio:str | None) -> Profile:
    return Profile.objects.create(user=user, bio=bio)
    
def create_user(*, username:str, email:str, password:str) -> BaseUser:
    return BaseUser.objects.create_user(username=username, email=email, password=password)

@transaction.atomic # If any step fails, the entire operation is rolled back
def register(*, bio:str, username:str, email:str, password:str) -> BaseUser:
    user = create_user(username=username, email=email, password=password)
    create_profile(user=user, bio=bio)

    return user