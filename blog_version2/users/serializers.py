from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import BaseUser


class RegisterInputSerializer(serializers.ModelSerializer):
    password = serializers.CharField(validators=[validate_password])
    confirm_password = serializers.CharField()

    class Meta:
        model = BaseUser
        fields = ("username", "email", "password", "confirm_password",)

    def validate(self, attrs:dict):
        if attrs.get("password") != attrs.get("confirm_password"):
            raise ValidationError({"confirm_password": "password and confirm password not match!"})

        attrs.pop("confirm_password")
        return super().validate(attrs)
    

class RegisterOutputSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BaseUser
        fields = ("username", "email", "created_at",)

    