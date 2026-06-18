from django.urls import path
from blog_version2.users.apis import RegisterAPIView, ProfileAPIView



urlpatterns = [
    path(route="register/", view=RegisterAPIView.as_view(), name="register"),
    path(route="profile/", view=ProfileAPIView.as_view(), name="profile"),
]