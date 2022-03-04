from rest_framework import serializers
from rest_flex_fields.serializers import FlexFieldsSerializerMixin

from core.models import User
from freeradius.models import Device, CsvImporter

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'email', 'first_name', 'last_name', 'groups']

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = [
            'mac',
            'created_at',
            'updated_at',
            'hostname',
            'description',
            'import_source',
        ]
