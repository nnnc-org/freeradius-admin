from rest_framework import serializers
from rest_flex_fields.serializers import FlexFieldsSerializerMixin
from rest_flex_fields import FlexFieldsModelSerializer

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

        read_only_fields = (
            'created_at',
            'updated_at',
            'import_source',
        )

class DeviceMacSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = [
            'mac',
        ]

class CsvImporterSerializer(FlexFieldsModelSerializer):
    device_count = serializers.IntegerField(
        source='devices.count',
        read_only=True
    )

    class Meta:
        model = CsvImporter
        fields = [
            'id',
            'created_at',
            'updated_at',
            'csvfile',
            'overwrite',
            'mac_header',
            'hostname_header',
            'description_header',
            'device_count',
        ]

        expandable_fields = {
            'devices': (DeviceSerializer, {'many': True})
        }
