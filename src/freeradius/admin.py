from django.contrib import admin

from .models import Device,CsvImporter
from . import tasks

class DeviceAdmin(admin.ModelAdmin):
    list_display = ('mac', 'hostname', 'description', 'created_at')
    list_filter = ('created_at', )

# Admin Action Functions
def process_csv(modeladmin, request, queryset):
    for obj in queryset:
        tasks.process_import(obj.id)

class CsvAdmin(admin.ModelAdmin):
    list_display = ('id', 'csvfile', 'devices_count', 'created_at')
    list_filter = ('created_at', )
    actions = [process_csv]

    def devices_count(self, obj):
        return obj.devices.count()

admin.site.register(Device, DeviceAdmin)
admin.site.register(CsvImporter, CsvAdmin)