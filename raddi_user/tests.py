# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import copy

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from raddi_user.models import User


class UserAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test', password='abc', phone='1111111111', email='test@s.com',
                                        address='joh')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def update_data(self, dict):
        temp = copy.deepcopy(self.user.user_details())

        for (key, value) in dict.items():
            temp[key] = value

        return temp

    def test_update_phone(self):
        response = self.client.put(
            reverse('user-detail', kwargs={'pk': self.user.id}),
            data=self.update_data({'phone': '1111111112'}),
            format='json'
        )
        self.user.refresh_from_db()
        self.assertEqual(self.user.phone, "1111111112")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        response = self.client.put(
            reverse('user-detail', kwargs={'pk': self.user.id}),
            data=self.update_data({'phone': 'edd'})
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_email(self):
        response = self.client.put(
            reverse('user-detail', kwargs={'pk': self.user.id}),
            data=self.update_data({'email': 'test@raddiwala.com'})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "test@raddiwala.com")


        response = self.client.put(
            reverse('user-detail', kwargs={'pk': self.user.id}),
            data=self.update_data({'email': 'edd'})
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
