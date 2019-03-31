import re

from rest_framework import serializers
from .models import User

from rest_framework.exceptions import (
    ValidationError,
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'phone', 'address', 'first_name', 'last_name', 'email')
        read_only_fields = ('username', )
        extra_kwargs = {
            'phone': {'required': True},
            'address': {'required': True},
            'email': {'required': True}
        }


    def validate(self, data):
        regex = re.compile("\d{10}$")

        if not regex.match(data["phone"]):
            raise ValidationError('Enter valid phone number')

        if not re.compile("^\S+@\S+$").match(data["email"]):
            raise ValidationError("Invalid Email")

        return data
