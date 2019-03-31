# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import WasteSerializer
from .models import Waste


class WasteViewSet(ModelViewSet):
    serializer_class = WasteSerializer
    permission_classes = (IsAuthenticated, )

    queryset = Waste.objects.all()
