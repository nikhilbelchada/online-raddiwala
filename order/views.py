# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv

from django.http import HttpResponse
from django.utils import timezone
from dateutil import parser

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, list_route
from rest_framework import status


from .serializers import (
    OrderSerializer,
    OrderFeedbackReplySerializer,
)

from .models import Order

from rest_framework import (
    mixins,
    viewsets,
)


class OrderViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, )

    csv_fields = ['username', 'status', 'amount_paid', 'order_date', 'pickup_date', 'feedback']

    def get_queryset(self):
        user = self.request.user
        params = self.request.query_params
        filters = {}

        if not user.is_admin:
            filters.update({'user_id': user.id})

        if params.get('status'):
            filters.update({'status': params.get('status')})

        return Order.objects.filter(**filters).order_by('-updated_at')

    @list_route(methods=['get'], url_path='download-report')
    def download_report(self, request):
        data = self.get_queryset()
        serializer = self.get_serializer(data, many=True)
        date_format = "%d-%m-%Y %H:%M:%S"

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'

        writer = csv.DictWriter(response, fieldnames=self.csv_fields)
        writer.writeheader()

        for row in serializer.data:
            data = {}

            for field in self.csv_fields:
                if 'date' in field:
                    data[field] = timezone.datetime.strftime(parser.parse(row[field]), date_format)
                else:
                    data[field] = row[field]

            writer.writerow(data)


        return response


    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user

        data = {}

        status = request.data.get("status")
        if status:
            data.update({'status': status})

        pickup_date = request.data.get("pickup_date")
        if status:
            data.update({'pickup_date': pickup_date})

        feedback = request.data.get("feedback")
        if status:
            data.update({'feedback': feedback})

        amount_paid = request.data.get("amount_paid")
        if amount_paid:
            data.update({'amount_paid': amount_paid})

        reply = request.data.get("reply")
        if reply:
            data.update({'reply': reply})

        order_items = request.data.get("order_items")
        if order_items:
            data.update({'order_items': order_items})

        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


@api_view(['PUT'])
@permission_classes((IsAuthenticated, ))
def feedback_reply_view(request, pk):
    try:
        if(request.user.is_admin):
            order = Order.objects.get(pk=pk)
        else:
            order = Order.objects.get(pk=pk, user=request.user)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = OrderFeedbackReplySerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_404_NOT_FOUND)
