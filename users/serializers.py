from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from .validators import *


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    
    Handles validation for:
    - Username rules (via custom validator)
    - Email uniqueness
    - Password strength and match confirmation

    On successful validation, creates a new user using the custom user model.
    """

    username = serializers.CharField(validators=[validate_username])
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']


    def validate_email(self, value):
        """
        Ensure email is unique (case-insensitive).
        """
         
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value
    

    def validate(self, data):
        """
        Perform cross-field validation:
        - Passwords must match
        - Password must meet strength requirements 
        """

        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        try:
            validate_password(data['password'])
        except DjangoValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        return data


    def create(self, validated_data):
        """
        Create and return a new user after removing confirm_password.
        """
        validated_data.pop('confirm_password')  # not needed for user creation so remove it
        user = User.objects.create_user(**validated_data)
        return user