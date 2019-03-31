from rest_framework import serializers
from .models import Waste

from rest_framework.exceptions import (
    ValidationError,
)

class WasteSerializer(serializers.ModelSerializer):
    waste_category_name = serializers.ReadOnlyField(source='waste_category.name')
    class Meta:
        model = Waste
        fields = ('id', 'name', 'description', 'price', 'unit', 'waste_category', 'created_at', 'updated_at',
                  'waste_category_name')
        extra_kwargs = {
            'name': {'required': True},
            'unit': {'required': True},
            'price': {'required': True}
        }


    def validate(self, data):
        if not data["price"] or data["price"] <= 0:
            raise ValidationError('Price should be greater than 0')

        return data
