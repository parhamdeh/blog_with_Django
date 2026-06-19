

from django.urls import path, include

from .apis.posts import PostAPIView, PostRetrievUpdateDestroy
from .apis.subscription import SubscribeAPIView, SubscribeDtailAPIView

app_name = "home"
urlpatterns = [
    path(route="subscribe/", view=SubscribeAPIView.as_view(), name="subscribe"),
    path(route="unsubscribe/", view=SubscribeDtailAPIView.as_view(), name="unsubscribe"),
    path(route="", view=PostAPIView.as_view(), name="post"),
    path(route="post/<slug:slug>", view=PostRetrievUpdateDestroy.as_view(), name="post-detail"),
]