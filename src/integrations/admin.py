from django.contrib import admin
from .models import MosyleIntegration, GoogleIntegration

def run_integration(modeladmin, request, queryset):
    for obj in queryset:
        obj.process()

class MosyleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'devices_count', 'created_at', 'enabled')
    list_filter = ('created_at', )
    actions = [run_integration]

    def devices_count(self, obj):
        return obj.devices.count()

class GoogleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'devices_count', 'created_at', 'enabled')
    list_filter = ('created_at', )
    actions = [run_integration]

    def devices_count(self, obj):
        return obj.devices.count()

admin.site.register(MosyleIntegration, MosyleAdmin)
admin.site.register(GoogleIntegration, GoogleAdmin)
