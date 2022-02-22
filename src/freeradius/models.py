from django.db import models
from datetime import datetime
from macaddress.fields import MACAddressField
#import csv


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