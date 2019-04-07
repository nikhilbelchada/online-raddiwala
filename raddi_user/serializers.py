import re

from rest_framework import serializers
from .models import User

from rest_framework.exceptions import (
    ValidationError,
)

class UserSerializer(serializers.ModelSerializer):
    admin = serializers.ReadOnlyField(source='is_admin')

    class Meta:
        model = User
        fields = ('id', 'username', 'phone', 'address', 'first_name', 'last_name', 'email', 'password', 'admin')
        extra_kwargs = {
            'username': {'required': True},
            'phone': {'required': True},
            'address': {'required': True},
            'email': {'required': True},
            'password': {'required': False},
        }


    def validate(self, data):
        regex = re.compile("\d{10}$")

        if not regex.match(data["phone"]):
            raise ValidationError('Enter valid phone number')

        if not re.compile("^\S+@\S+$").match(data["email"]):
            raise ValidationError("Invalid Email")

        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=False, allow_blank=True)
    new_password = serializers.CharField(required=True)

    def validate(self, data):
        if not data["new_password"]:
            raise ValidationError("New Password not provided")

        if len(data["new_password"]) < 6:
            raise ValidationError("New Password must be min 6 characters")

        if not self.context['request'].user.is_admin:
            if data["old_password"] == data["new_password"]:
                raise ValidationError("Old Password and New Password cannot be same")

            if not data["old_password"]:
                raise ValidationError("Old Password not provided")

        return data

    def save(self):
        old_password = self.validated_data["old_password"]
        new_password = self.validated_data["new_password"]

        user = self.context['user']
        request_user = self.context['request'].user

        if not request_user.is_admin and not user.check_password(old_password):
            raise ValidationError("Invalid Old Password")

        user.set_password(new_password)
        user.save()
