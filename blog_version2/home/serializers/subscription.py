from rest_framework import serializers

from blog_with_Django.blog_version2.home.models import Subscription


class SubscribeInputSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)

class SubscribeOutputSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField("get_username")

    class Meta:
        model = Subscription
        fields = ("email", )

    def get_username(self, subscription):
        return subscription.target.username