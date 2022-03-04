from django_filters import rest_framework as filters
import re
from freeradius.models import Device

class DeviceFilter(filters.FilterSet):   
    
    mac = filters.CharFilter(field_name='mac', method='filter_mac')

    # make sure to convert any ":", ".", or other weird chars to "-"
    def filter_mac(self, queryset, name, value):
        if value is not None:
            queryset = queryset.filter(mac__icontains=re.sub('\W+', ':', value))
        return queryset
    
    class Meta:
        model = Device
        fields = ['mac', 'created_at', 'updated_at', 'hostname', 'description', 'import_source']