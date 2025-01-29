from . import BaseIntegration
from fernet_fields import EncryptedTextField
from django.db import models
import requests
from requests.auth import HTTPBasicAuth
from operator import itemgetter

class MosyleIntegrationModel(BaseIntegration):
    accessToken = EncryptedTextField()
    username = models.CharField(max_length=255)
    password = EncryptedTextField()

    apiURL = models.CharField(max_length=255, default="https://managerapi.mosyle.com/v2")

    def process(self):

        def apiCall(self, options):
            # cycle through pages of devices
            return requests.post(
                self.apiURL + "/listdevices", 
                auth=HTTPBasicAuth(self.username,self.password), 
                json = {
                    'accessToken' : self.accessToken, 
                    'options' : options
                }
            ).json()
        
        def cyclePages(self, options):

            response = apiCall(self, options)
            devices = response['response']['devices']

            # check for more pages
            while response['response']['page_size'] * response['response']['page'] < response['response']['rows']:
                options['page'] = options['page'] + 1
                response = apiCall(self, options)
                devices = devices + response['response']['devices']
            return devices


        # get devices from Mosyle
        ipads = cyclePages(self, {'os': 'ios', 'page': 1})
        macs = cyclePages(self, {'os': 'mac', 'page': 1})

        print("ipads: " + str(len(ipads)))
        print("macs: " + str(len(macs)))

        # add devices to integration
        for ipad in ipads:
            if ipad['wifi_mac_address']:
                self.add_device_raw(ipad['wifi_mac_address'], ipad['device_name'], "iPad WiFi")
            if ipad['ethernet_mac_address']:
                self.add_device_raw(ipad['ethernet_mac_address'], ipad['device_name'], "iPad Ethernet")
        
        for mac in macs:
            if mac['wifi_mac_address']:
                self.add_device_raw(mac['wifi_mac_address'], mac['device_name'], "Mac WiFi")
            if mac['ethernet_mac_address']:
                self.add_device_raw(mac['ethernet_mac_address'], mac['device_name'], "Mac Ethernet")
        
        #remove devices from integration
        for d in self.devices.all():
            if d.pk in list(map(itemgetter('wifi_mac_address'), ipads)):
                continue
            elif d.pk in list(map(itemgetter('ethernet_mac_address'), ipads)):
                continue
            elif d.pk in list(map(itemgetter('wifi_mac_address'), macs)):
                continue
            elif d.pk in list(map(itemgetter('ethernet_mac_address'), macs)):
                continue
            else:
                self.remove_device(self, d.mac)
        
        return

