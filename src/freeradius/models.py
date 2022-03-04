from django.db import models
from datetime import datetime
from django.contrib.postgres.fields import ArrayField
from netfields import MACAddressField
#from macaddress.fields import MACAddressField
import csv


# Mixin for models
class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Device(TimeStampMixin):
    mac = MACAddressField(primary_key=True,unique=True)
    hostname = models.CharField(max_length=253, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    SOURCE_MANUAL = 'MN'
    SOURCE_API = 'AP'
    SOURCE_CSV = 'CV'

    SOURCE_CHOICES = [
        (SOURCE_MANUAL, "Manual"),
        (SOURCE_API, "API"),
        (SOURCE_CSV, "CSV"),
    ]

    import_source = models.CharField(max_length=2, choices=SOURCE_CHOICES, default=SOURCE_MANUAL)

class CsvImporter(TimeStampMixin):
    id = models.AutoField(primary_key=True)
    csvfile = models.FileField(upload_to='uploads/%Y/%m/%d/')
    overwrite = models.BooleanField(default=True, help_text="Overwrite existing hostname & description?")

    # Header Fields to map the CSV to device values. MAC required, not others
    mac_header = models.CharField(max_length=254, default="mac")
    hostname_header = models.CharField(max_length=254, blank=True, null=True)
    description_header = models.CharField(max_length=254, blank=True, null=True)

    # Internal Model Data
    error_messages = ArrayField(models.TextField(), blank=True, null=True)
    devices = models.ManyToManyField(Device, blank=True, null=True)
    manual_upload = models.BooleanField(default=True)

    def process(self):
        with self.csvfile.open('r') as csvfile:
            devicereader = csv.DictReader(csvfile)

            for row in devicereader:
                # TODO: add errors to error_messages

                mac = row[self.mac_header]

                device = Device.objects.filter(pk=mac).first()

                if not device:
                    device = Device(mac=mac, import_source=Device.SOURCE_CSV)
                    if hostname_header:
                        device.hostname = row[self.hostname_header]
                    if description_header:
                        device.description = row[self.description_header]
                    device.save()
                elif overwrite:
                    if hostname_header:
                        device.hostname = row[self.hostname_header]
                    if description_header:
                        device.description = row[self.description_header]
                    device.save()

                # Add device to devices
                self.devices.add(device)
        return

"""
class PostAuthLog(TimeStampMixin):
    username = models.CharField(verbose_name=_('username'), max_length=64)
    reply = models.CharField(verbose_name=_('reply'), max_length=32)
    called_station_id = models.CharField(
        verbose_name=_('called station ID'),
        max_length=50,
        blank=True,
        null=True,
    )
    calling_station_id = models.CharField(
        verbose_name=_('calling station ID'),
        max_length=50,
        blank=True,
        null=True,
    )
    date = models.DateTimeField(
        verbose_name=_('date'), auto_now_add=True
    )

    def __str__(self):
        return str(self.username)
"""