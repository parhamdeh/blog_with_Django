

from django.urls import reverse
from rest_framework import serializers

from blog_version2.home.models import Posts


class FilterPostSerializer(serializers.Serializer):
    title = serializers.CharField(required=False, max_length=100)
    search = serializers.CharField(required=False, max_length=100)
    created_at__range = serializers.CharField(required=False, max_length=100)
    author__in = serializers.CharField(required=False, max_length=20)
    slug = serializers.CharField(required=False, max_length=100)
    content = serializers.CharField(required=False, max_length=1000)

class PostInputSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=1000)
    title = serializers.CharField(max_length=100)

class PostOutputSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField("get_author")
    url = serializers.SerializerMethodField("get_url")

    class Meta:
        model = Posts
        fields = ("url", "title", "author", "content",)
        
    def get_author(self, post):
        return post.author.username
    
    def get_url(self, post):
        request = self.context.get("request")
        path = reverse("api:home:post_detail", args=(post.slug, ))
        return request.build_absolute_uri(path)
    

class PostDetailOutputSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField("get_author")
    
    class Meta:
        model = Posts
        fields = ("title", "author", "content", "created_at", "updated_at",)
        
    def get_author(self, post):
        return post.author.username