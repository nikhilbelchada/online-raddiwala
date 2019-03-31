# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from waste_category.models import WasteCategory
from waste.models import Waste
from .models import (
    Order,
    OrderItem,
)
from .serializers import OrderSerializer
from raddi_user.models import User

from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


class OrderAPITest(APITestCase):
    def setUp(self):
        self.waste_category = WasteCategory.objects.create(name='Metal', description='Metal Wastes')
        self.iron_waste = Waste.objects.create(
            name='Iron', description='Iron Waste', price=10.0,
            unit='kg', waste_category=self.waste_category,
        )
        self.silver_waste = Waste.objects.create(
            name="Silver", description="Silver Waste", price=20.0, unit='kg',
            waste_category=self.waste_category,
        )

        self.user = User.objects.create(username='test', password='abc')
        self.admin_user = User.objects.create(username='admin', password='abc', is_superuser=True)
        self.token = Token.objects.create(user=self.user)
        self.admin_token = Token.objects.create(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_should_not_all_unauthorized_access(self):
        self.client.credentials()
        response = self.client.get(reverse('order-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_create_order_with_proper_order_items(self):
        order = {
            'user': self.user.id,
            'pickup_date': timezone.now(),
            'order_items': [
                {'waste': self.iron_waste.id, 'quantity': 1.0},
                {'waste': self.silver_waste.id, 'quantity': 1.0},
            ],
        }
        response = self.client.post(reverse('order-list'), data=order, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 2)

    def test_should_create_order_with_status_created(self):
        order = {
            'user': self.user.id,
            'pickup_date': timezone.now(),
            'status': 'COMPLETE',
            'order_items': [
                {'waste': self.iron_waste.id, 'quantity': 1.0},
                {'waste': self.silver_waste.id, 'quantity': 1.0},
            ],
        }
        response = self.client.post(reverse('order-list'), data=order, format='json')
        self.assertEqual(Order.objects.get(id=response.data.get('id')).status, 'CREATED')

    def test_should_not_create_order_with_feedback(self):
        order = {
            'user': self.user.id,
            'pickup_date': timezone.now(),
            'feedback': 'good service',
            'order_items': [
                {'waste': self.iron_waste.id, 'quantity': 1.0},
                {'waste': self.silver_waste.id, 'quantity': 1.0},
            ],
        }
        response = self.client.post(reverse('order-list'), data=order, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data['feedback'][0]), 'You cannot give feedback unless order is complete')

    def test_should_not_create_order_with_reply(self):
        order = {
            'user': self.user.id,
            'pickup_date': timezone.now(),
            'reply': 'reply',
            'order_items': [
                {'waste': self.iron_waste.id, 'quantity': 1.0},
                {'waste': self.silver_waste.id, 'quantity': 1.0},
            ],
        }
        response = self.client.post(reverse('order-list'), data=order, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data['reply'][0]), 'You cannot reply to order unless complete')

    def test_should_not_allow_normal_user_to_update_reply(self):
        order = {
            'user': self.user.id,
            'pickup_date': timezone.now(),
            'order_items': [
                {'waste': self.iron_waste.id, 'quantity': 1.0},
                {'waste': self.silver_waste.id, 'quantity': 1.0},
            ],
        }
        serializer = OrderSerializer(data=order)
        if serializer.is_valid():
            serializer.save()

        data = serializer.data
        data.update({'reply': 'reply'})

        response = self.client.put(
            reverse('order-detail', kwargs={'pk': data['id']}), data=data, format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data['reply'][0]), 'You donot have permission to update reply')

    def test_should_update_order_status(self):
        order = {
            'user': self.user.id,
            'pickup_date': timezone.now(),
            'order_items': [
                {'waste': self.iron_waste.id, 'quantity': 1.0},
                {'waste': self.silver_waste.id, 'quantity': 1.0},
            ],
        }
        serializer = OrderSerializer(data=order)
        if serializer.is_valid():
            serializer.save()

        data = serializer.data
        data.update({'status': 'CANCELLED'})

        response = self.client.put(
            reverse('order-detail', kwargs={'pk': data['id']}), data=data, format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_not_allow_normal_user_to_complete_order(self):
        order = {
            'user': self.user.id,
            'pickup_date': timezone.now(),
            'order_items': [
                {'waste': self.iron_waste.id, 'quantity': 1.0},
                {'waste': self.silver_waste.id, 'quantity': 1.0},
            ],
        }
        serializer = OrderSerializer(data=order)
        if serializer.is_valid():
            serializer.save()

        data = serializer.data
        data.update({'status': 'COMPLETE'})

        response = self.client.put(
            reverse('order-detail', kwargs={'pk': data['id']}), data=data, format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data['status'][0]), 'You donot have permission to mark order complete')

    def test_should_allow_admin_to_complete_order(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)

        order = {
            'user': self.admin_user.id,
            'pickup_date': timezone.now(),
            'order_items': [
                {'waste': self.iron_waste.id, 'quantity': 1.0},
                {'waste': self.silver_waste.id, 'quantity': 1.0},
            ],
        }
        serializer = OrderSerializer(data=order)
        if serializer.is_valid():
            serializer.save()

        data = serializer.data
        data.update({'status': 'COMPLETE'})

        response = self.client.put(
            reverse('order-detail', kwargs={'pk': data['id']}), data=data, format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Order.objects.get(id=response.data.get('id')).status, 'COMPLETE')

    def test_should_not_allow_normal_user_to_accept_order(self):
        order = {
            'user': self.user.id,
            'pickup_date': timezone.now(),
            'order_items': [
                {'waste': self.iron_waste.id, 'quantity': 1.0},
                {'waste': self.silver_waste.id, 'quantity': 1.0},
            ],
        }
        serializer = OrderSerializer(data=order)
        if serializer.is_valid():
            serializer.save()

        data = serializer.data
        data.update({'status': 'ACCEPTED'})

        response = self.client.put(
            reverse('order-detail', kwargs={'pk': data['id']}), data=data, format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data['status'][0]), 'You donot have permission to accept order')

    def test_should_allow_admin_to_accept_order(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)

        order = {
            'user': self.admin_user.id,
            'pickup_date': timezone.now(),
            'order_items': [
                {'waste': self.iron_waste.id, 'quantity': 1.0},
                {'waste': self.silver_waste.id, 'quantity': 1.0},
            ],
        }
        serializer = OrderSerializer(data=order)
        if serializer.is_valid():
            serializer.save()

        data = serializer.data
        data.update({'status': 'ACCEPTED'})

        response = self.client.put(
            reverse('order-detail', kwargs={'pk': data['id']}), data=data, format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Order.objects.get(id=response.data.get('id')).status, 'ACCEPTED')
