

from django.contrib.auth.password_validation import validate_password
from django.core.validators import MinLengthValidator

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from blog_version2.users.validators import LetterValidator, NumberValidator, SpecialCharValidator
from blog_version2.users.models import BaseUser, Profile



class RegisterInputSerializer(serializers.ModelSerializer):
    password = serializers.CharField(validators=[
                                                validate_password,
                                                MinLengthValidator(limit_value=10),
                                                LetterValidator(),
                                                NumberValidator(),
                                                SpecialCharValidator()
                                                ])
    confirm_password = serializers.CharField()
    bio = serializers.CharField(max_length=1000, required=False)

    class Meta:
        model = BaseUser
        fields = ("username", "email", "password", "confirm_password", "bio")

    def validate_email(self, email:str):
        if BaseUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("email already taken")
        return email
        
    def validate_username(self, username:str):
        if BaseUser.objects.filter(email=username).exists():
            raise serializers.ValidationError("username already taken")
        return username

    def validate(self, attrs:dict):
        if attrs.get("password") != attrs.get("confirm_password"):
            raise ValidationError({"confirm_password": "password and confirm password not match!"})

        attrs.pop("confirm_password")
        return super().validate(attrs)
    

class RegisterOutputSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BaseUser
        fields = ("username", "email", "created_at",)

    
class ProfileOutputSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = ("bio", "posts_count", "subscriber_count", "subscription_count")

    