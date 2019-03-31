# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.urls import reverse

from .models import WasteCategory
from raddi_user.models import User
from .serializers import WasteCategorySerializer

from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework.test import force_authenticate
from rest_framework.authtoken.models import Token


class WasteCategoryTest(TestCase):
    def setUp(self):
        self.waste_category = WasteCategory.objects.create(name='Metal', description='Metal Wastes')

    def test_waste_cateogry_name(self):
        metal_waste_category = WasteCategory.objects.first()
        self.assertEqual(metal_waste_category.name, "Metal")

    def test_waste_cateogry_description(self):
        metal_waste_category = WasteCategory.objects.first()
        self.assertEqual(metal_waste_category.description, "Metal Wastes")


class WaasteCategoryAPITest(APITestCase):
    def setUp(self):
        self.waste_category = WasteCategory.objects.create(name='Metal', description='Metal Wastes')
        self.user = User.objects.create(username='test', password='abc')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_should_not_all_unauthorized_access(self):
        self.client.credentials()
        response = self.client.get(reverse('waste-category-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_all_waste_categories(self):
        response = self.client.get(reverse('waste-category-list'))

        waste_categories = WasteCategory.objects.all()
        serializer = WasteCategorySerializer(waste_categories, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_waste_category(self):
        response = self.client.get(reverse('waste-category-detail', kwargs={'pk': self.waste_category.id}))

        waste_category = WasteCategory.objects.get(id=self.waste_category.id)
        serializer = WasteCategorySerializer(waste_category)

        self.assertEqual(response.data, serializer.data)

    def test_create_waste_category(self):
        response = self.client.post(
            reverse('waste-category-list'),
            data={'name': 'New Waste', 'description': 'Newly added'},
            format='json'
        )

        waste_category = WasteCategory.objects.last()
        serializer = WasteCategorySerializer(waste_category)

        self.assertEqual(response.data, serializer.data)

    def test_not_create_waste_category_for_invalid_data(self):
        response = self.client.post(reverse('waste-category-list'), data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(reverse('waste-category-list'), data={'name': "abc"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(reverse('waste-category-list'), data={'description': "sbc"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_waste_category(self):
        waste_category = WasteCategory.objects.first()

        response = self.client.put(
            reverse('waste-category-detail', kwargs={'pk': waste_category.id}),
            data={'name': 'Updated Waste', 'description': 'Updated Description'},
            format='json'
        )

        waste_category = WasteCategory.objects.get(id=waste_category.id)
        serializer = WasteCategorySerializer(waste_category)

        self.assertEqual(response.data, serializer.data)

    def test_not_update_waste_category_invalid_data(self):
        response = self.client.put(
            reverse('waste-category-detail', kwargs={'pk': self.waste_category.id}),
            data={},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.put(
            reverse('waste-category-detail', kwargs={'pk': self.waste_category.id}),
            data={'name': "name"},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.put(
            reverse('waste-category-detail', kwargs={'pk': self.waste_category.id}),
            data={'description': "desc"},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_waste_category(self):
        waste_category = WasteCategory.objects.first()

        response = self.client.delete(
            reverse('waste-category-detail', kwargs={'pk': waste_category.id}),
        )

        waste_category_count = WasteCategory.objects.filter(id=waste_category.id).count()

        self.assertEqual(waste_category_count, 0)
