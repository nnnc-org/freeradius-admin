from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework import permissions, renderers
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from netfields.rest_framework import MACAddressField
import re

from .serializers import UserSerializer, DeviceSerializer, CsvImporterSerializer, PostAuthLogSerializer
from .filters import DeviceFilter
from core.models import User
from freeradius.models import Device, CsvImporter, PostAuthLog
from freeradius import tasks

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed, created, destroyed, or modified.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'

class DeviceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows devices to be viewed, created, destroyed, or modified.
    """
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [permissions.IsAuthenticated]
    #lookup_field = 'mac'
    #lookup_value_regex = '\W+'
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = DeviceFilter
    #filterset_fields = ('mac', 'created_at', 'updated_at', 'hostname', 'import_source') 
    ordering_fields = ('mac', 'created_at', 'updated_at', 'hostname', 'import_source')
    ordering = ('created_at')

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        # allow more dynamic lookups - replace any weird chars with :
        # allows 00-00-00-00-00 or 00.00.00.00.00.00 as valid attempts
        filter_kwargs = {self.lookup_field: re.sub('\W+', ':', self.kwargs[lookup_url_kwarg])}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def perform_create(self, serializer):
        serializer.save(import_source=Device.SOURCE_API)

class CsvImporterViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows csv_imports to be viewed, created, destroyed, or modified.
    """
    queryset = CsvImporter.objects.all()
    serializer_class = CsvImporterSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = ('id', 'created_at', 'updated_at', 'device__count')
    filterset_fields = ('id', 'created_at', 'updated_at')

    ordering = ('-created_at')
    
    def get_serializer_context(self):
        return {'request': self.request}

    @action(detail=True)
    def process(self, request, *args, **kwargs):
        obj = self.get_object()
        t = tasks.process_import(obj.id)
        content = {'status': "accepted", 'task_id': t.id}
        return Response(content, status=status.HTTP_202_ACCEPTED)

class PostAuthLogViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows PostAuthLog to be viewed, created, destroyed, or modified.
    """
    queryset = PostAuthLog.objects.all()
    serializer_class = PostAuthLogSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)

    ordering = ('-created_at')

    def update(self, request, pk=None):
        response = {'message': 'Update function is not offered in this path.'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk=None):
        response = {'message': 'Update function is not offered in this path.'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk=None):
        response = {'message': 'Delete function is not offered in this path.'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)