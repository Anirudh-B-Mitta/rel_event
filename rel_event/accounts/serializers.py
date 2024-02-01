# serializers.py
from rest_framework import serializers
from .models import CustomUser
from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','email','name','password','profile_pic']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name'],
            profile_pic=validated_data['profile_pic'],
        )
        return user


User = get_user_model()

class PasswordUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password',)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        return super().update(instance, validated_data)
