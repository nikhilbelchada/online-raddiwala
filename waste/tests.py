# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import copy

from django.test import TestCase

from django.urls import reverse

from .models import (
    WasteCategory,
    Waste,
)
from .serializers import WasteSerializer
from raddi_user.models import User

from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


class WasteTest(TestCase):
    def setUp(self):
        self.waste_category = WasteCategory.objects.create(name='Metal', description='Metal Wastes')
        self.waste = Waste.objects.create(
            name='Iron', description='Iron Waste', price=10.0, unit='Kg', waste_category=self.waste_category
        )

    def test_waste_name(self):
        metal_waste = Waste.objects.first()
        self.assertEqual(metal_waste.name, "Iron")

    def test_waste_description(self):
        metal_waste = Waste.objects.first()
        self.assertEqual(metal_waste.description, "Iron Waste")

    def test_waste_price(self):
        metal_waste = Waste.objects.first()
        self.assertEqual(metal_waste.price, 10.0)

    def test_waste_unit(self):
        metal_waste = Waste.objects.first()
        self.assertEqual(metal_waste.unit, "Kg")

    def test_waste_waste_category(self):
        metal_waste = Waste.objects.first()
        self.assertEqual(metal_waste.waste_category_id, self.waste_category.id)


class WasteAPITest(APITestCase):
    def setUp(self):
        self.waste_category = WasteCategory.objects.create(name='Metal', description='Metal Wastes')
        self.waste = Waste.objects.create(name='Iron', description='Iron Waste', price=10.0, unit='kg',
                                          waste_category=self.waste_category)
        Waste.objects.create(name="Silver", description="Silver Waste", price=20.0, unit='kg',
                             waste_category=self.waste_category)
        self.user = User.objects.create(username='test', password='abc')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_should_not_all_unauthorized_access(self):
        self.client.credentials()
        response = self.client.get(reverse('waste-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_all_waste(self):
        response = self.client.get(reverse('waste-list'))

        wastes = Waste.objects.all()
        serializer = WasteSerializer(wastes, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_waste(self):
        response = self.client.get(reverse('waste-detail', kwargs={'pk': self.waste.id}))

        waste = Waste.objects.get(id=self.waste.id)
        serializer = WasteSerializer(waste)

        self.assertEqual(response.data, serializer.data)

    def test_create_waste(self):
        response = self.client.post(
            reverse('waste-list'),
            data={'name': 'Aluminium', 'description': 'Aluminium Waste', 'price': 20.0, 'unit': 'Kg',
                  'waste_category': self.waste_category.id},
            format='json'
        )

        waste = Waste.objects.last()
        serializer = WasteSerializer(waste)

        self.assertEqual(response.data, serializer.data)

    def test_update_waste(self):
        response = self.client.put(
            reverse('waste-detail', kwargs={'pk': self.waste.id}),
            data={'name': 'Aluminium', 'description': 'Aluminium Waste', 'price': 20.0, 'unit': 'Kg',
                  'waste_category': self.waste_category.id}
        )

        waste = Waste.objects.get(id=self.waste.id)
        serializer = WasteSerializer(waste)

        self.assertEqual(response.data, serializer.data)

    def test_delete_waste(self):
        response = self.client.delete(reverse('waste-detail', kwargs={'pk': self.waste.id}))
        waste_count = Waste.objects.filter(id=self.waste.id).count()

        self.assertEqual(waste_count, 0)

    def test_invalid_values(self):
        def build_data(name, description, price, unit, waste_category_id):
            return {'name': name, 'description': description, 'price': price, 'unit': unit,
                    'waste_category': waste_category_id}

        def update_data(data, dict):
            temp = copy.deepcopy(data)
            for (key, value) in dict.items():
                temp[key] = value
            return temp

        data = build_data("Aluminium", "Aluminium Desc", 10.0, "kg", self.waste_category.id)

        # empty values
        response = self.client.post(reverse('waste-list'), data=update_data(data, {"name": None}), format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(reverse('waste-list'), data=update_data(data, {"name": ""}), format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # empty unit
        response = self.client.post(reverse('waste-list'), data=update_data(data, {"unit": None}), format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(reverse('waste-list'), data=update_data(data, {"unit": ""}), format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # zero price
        response = self.client.post(reverse('waste-list'), data=update_data(data, {"price": 0.00}), format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # negative price
        response = self.client.post(reverse('waste-list'), data=update_data(data, {"price": -100.00}), format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # invalid category id
        response = self.client.post(
            reverse('waste-list'),
            data=update_data(data, {"waste_category": 0}),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(
            reverse('waste-list'),
            data=update_data(data, {"waste_category": None}),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # empty body
        response = self.client.post(reverse('waste-list'), data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
