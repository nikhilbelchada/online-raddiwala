from rest_framework import serializers
from .models import WasteCategory

class WasteCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteCategory
        fields = ('id', 'name', 'description', 'created_at', 'updated_at')
        extra_kwargs = {
            'name': {'required': True},
        }
