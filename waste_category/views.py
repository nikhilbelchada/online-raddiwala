# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import WasteCategorySerializer
from .models import WasteCategory


class WasteCategoryViewSet(ModelViewSet):
    serializer_class = WasteCategorySerializer
    permission_classes = (IsAuthenticated, )

    queryset = WasteCategory.objects.all()
