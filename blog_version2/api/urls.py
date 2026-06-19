from django.urls import path, include

urlpatterns = [
    path('users/', include(('blog_version2.users.urls'))),
    path('auth/', include(('blog_version2.authentication.urls'))),
    path('home/', include(('blog_version2.home.urls'))),
]
