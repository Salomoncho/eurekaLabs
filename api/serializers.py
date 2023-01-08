from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model

from api import api_messages


class RegisterSerializer(serializers.Serializer):
    """Register Serializer defines the Register API Structure"""
    name = serializers.CharField(max_length=100, required=True)
    last_name = serializers.CharField(max_length=100,  required=True)
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=get_user_model().objects.all(),
                message='This email address is already in the system, please use the login API'
                )],
        )
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Repeat Your Password'}
    )

    def validate(self, data):
        """ Function to compare Passwords"""
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": api_messages.REGISTER_PASSWORDS_DID_NOT_MATCH})
        return data


class LoginSerializer(serializers.ModelSerializer):
    """Login Serializer defines the Login API Structure"""
    class Meta:
        model = get_user_model()
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }
