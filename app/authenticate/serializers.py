from django.contrib.auth.models import User
from rest_framework import serializers

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериалайзер для создания нового пользователя"""
    password = serializers.CharField(write_only = True,required = True, style={'input_type':'password'})
    password2 = serializers.CharField(style={'input_type':'password'}, write_only = True, label ="confirm password")

    class Meta:
        model = User
        fields = ('username','email','password','password2',)
        extra_kwargs = {'password': {'write_only':True}}

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Password must match')
        return data
    
    def create(self, validated_data) -> User:
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password'],
        )
        return user