from django.urls import path, include

urlpatterns = [
    path('users/', include(('blog_version2.users.urls')))
]
