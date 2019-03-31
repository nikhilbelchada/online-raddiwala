from rest_framework import serializers
from .models import (
    STATUS_COMPLETE,
    STATUS_ACCEPTED,
    STATUS_CANCELLED,
    Order,
    OrderItem,
)

from rest_framework.exceptions import (
    ValidationError,
)


class OrderItemSerializer(serializers.ModelSerializer):
    waste_name = serializers.ReadOnlyField(source='waste.name')
    waste_unit = serializers.ReadOnlyField(source='waste.unit')
    waste_price = serializers.ReadOnlyField(source='waste.price')

    class Meta:
        model = OrderItem
        fields = '__all__'
        extra_kwargs = {'id': {'read_only': False, 'required': False}}


class OrderFeedbackReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'feedback', 'reply')


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        order_items = validated_data.pop('order_items')
        validated_data.pop('status', False)
        order = Order.objects.create(**validated_data)

        for order_item in order_items:
            OrderItem.objects.create(order=order, **order_item)

        return order

    def update(self, instance, validated_data):
        if instance.status == STATUS_COMPLETE:
            raise serializers.ValidationError("Cannot updated completed order")
        if instance.status == STATUS_CANCELLED:
            raise serializers.ValidationError("Cannot updated cancelled order")

        order_items = validated_data.pop('order_items')

        deleted_ids = set([i.id for i in instance.order_items.all()]) - set([i['id'] for i in order_items])
        for order_item in instance.order_items.all():
            if order_item.id in deleted_ids:
                order_item.delete()

        for order_item in instance.order_items.all():
            for i in order_items:
                if i['id'] == order_item.id:
                    order_item.quantity = i['quantity']
                    order_item.save()

        Order.objects.filter(id=instance.id).update(**validated_data)

        return instance

    def validate_order_items(self, value):
        if len(value) == 0:
            raise serializers.ValidationError("There must be one order item")

        return value

    def validate_pickup_date(self, value):
        if not self.instance and not value:
            raise serializers.ValidationError("Pickup date is mandatory")

        if self.instance and not value:
            value = self.instance.pickup_date

        return value

    def validate_status(self, value):
        if self.instance and self.instance.status != value:
            if value == STATUS_COMPLETE and not self.context['request'].user.is_admin:
                raise serializers.ValidationError("You donot have permission to mark order complete")
            if value == STATUS_ACCEPTED and not self.context['request'].user.is_admin:
                raise serializers.ValidationError("You donot have permission to accept order")

        return value

    def validate_feedback(self, value):
        if not self.instance and value:
            raise serializers.ValidationError("You cannot give feedback unless order is complete")

        return value

    def validate_reply(self, value):
        if value:
            if not self.instance:
                raise serializers.ValidationError("You cannot reply to order unless complete")

            if not self.context['request'].user.is_admin:
                raise serializers.ValidationError("You donot have permission to update reply")

        return value

    def validate_amount_paid(self, value):
        if not self.instance and value:
            raise serializers.ValidationError("You cannot set amount paid unless order is complete")

        if not self.context['request'].user.is_admin and self.instance.amount_paid != value:
            raise serializers.ValidationError("You donot have permission to update amount paid")

        return value
