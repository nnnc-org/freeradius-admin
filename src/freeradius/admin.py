from django.contrib import admin

from .models import Device,CsvImporter

admin.site.register(Device)
admin.site.register(CsvImporter)