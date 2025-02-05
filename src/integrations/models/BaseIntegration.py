import abc, datetime
from django.db import models
from django.contrib.postgres.fields import ArrayField
from freeradius.models import Device

class AbstractModelMeta(abc.ABCMeta, type(models.Model)):
    pass

class BaseIntegration(models.Model, metaclass=AbstractModelMeta):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    info_messages = ArrayField(models.TextField(), blank=True, null=True)
    enabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    devices = models.ManyToManyField(Device, blank=True, null=True)

    class Meta:
        abstract = True

    def remove_device(self, mac):
        # if the device is not in this integration, do nothing
        if not self.devices.filter(pk=mac).exists():
            return

        # get device
        d = self.devices.get(pk=mac)

        # remove device from devices
        self.devices.remove(d)
        self.save()

        # if the device was added by this integration and is not used by any other integrations, delete it
        if d.import_source == Device.SOURCE_INTEGRATION and d.integrations.count() == 0:
            d.delete()
        return

    def add_device(self, d: Device):
        # if the device was already added by this integration, do nothing
        if self.devices.filter(pk=d.pk).exists():
            return

        # add device to devices
        #self.info_messages.append("Added device '" + str(d.mac) + "' on " + str(datetime.datetime.now()))
        self.devices.add(d)
        self.save()
        return

    def add_device_raw(self, mac, hostname=None, description=None):
        # if the device was already added by this integration, do nothing
        if self.devices.filter(pk=mac).exists():
            return

        # if device already exists, add integration to device
        if Device.objects.filter(pk=mac).exists():
            d = Device.objects.get(pk=mac)
            self.add_device(d)
            return

        # else, create device and add integration to device
        d = Device(mac=mac, hostname=hostname, description=description, import_source=Device.SOURCE_INTEGRATION)
        d.save()
        self.add_device(d)

    @abc.abstractmethod
    def process(self):
        pass

    @property
    def model_name(self):
        return self.__class__.__name__
