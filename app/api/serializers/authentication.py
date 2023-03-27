from rest_framework import (
    serializers, exceptions
)
from app import models


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=4, max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=128)
    confirm_password = serializers.CharField(min_length=8, max_length=128)
    first_name = serializers.CharField(min_length=3, max_length=250,
                                       required=False)
    last_name = serializers.CharField(min_length=3, max_length=250,
                                      required=False)

    class Meta:
        model = models.User
        fields = [
            'username', 'email'
            'password', 'confirm_password',
        ]

    def validate(self, attrs):
        if (
            (attrs.get('password') != attrs.get('confirm_password')) or
            (attrs.get('password') is None) or ((attrs.get('email') is None))
        ):
            raise exceptions.NotAcceptable("Password and Confirm Password \
                                           mismatching")
        return True

    def create(self, validated_data):
        user = models.User.objects.create(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LogInSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=4, max_length=100,
                                     required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(min_length=8, max_length=100)

    def validate(self, attrs):
        email = attrs.get('email')
        username = attrs.get('username')
        password = attrs.get('password')

        if username is None and email is None:
            raise exceptions.NotAcceptable("Username or Email is required")
        if password is None:
            raise exceptions.NotAcceptable("Password is required")

        return attrs


class VerifyOTPSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    otp = serializers.CharField(min_length=6, max_length=6)


class ChangePasswordSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    old_password = serializers.CharField(min_length=8, max_length=128)
    new_password = serializers.CharField(min_length=8, max_length=128)
    confirm_password = serializers.CharField(min_length=8, max_length=128)

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        if new_password != confirm_password:
            raise exceptions.NotAcceptable(
                "Password and Confirm Password mismatching"
                )
        if old_password is None:
            raise exceptions.NotAcceptable("Old Password is required")
        if new_password is None:
            raise exceptions.NotAcceptable("New Password is required")

        return attrs


class ForgotPasswordSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    new_password = serializers.CharField(min_length=8, max_length=128)
    confirm_password = serializers.CharField(min_length=8, max_length=128)
    otp = serializers.CharField(min_length=6, max_length=6)

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        if new_password != confirm_password:
            raise exceptions.NotAcceptable(
                "Password and Confirm Password mismatching"
                )

        return attrs


class ForgotPasswordOTPSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
