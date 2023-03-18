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
    pass
