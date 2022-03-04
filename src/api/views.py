from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework import permissions, renderers
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from netfields.rest_framework import MACAddressField
import re

from .serializers import UserSerializer, DeviceSerializer
from .filters import DeviceFilter
from core.models import User
from freeradius.models import Device, CsvImporter
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
        """
        Returns the object the view is displaying.
        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: re.sub('\W+', ':', self.kwargs[lookup_url_kwarg])}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj