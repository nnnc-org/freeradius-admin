from . import BaseIntegration
from fernet_fields import EncryptedTextField
from django.db import models
import requests
from requests.auth import HTTPBasicAuth
from operator import itemgetter

class MosyleIntegration(BaseIntegration):
    accessToken = EncryptedTextField()
    username = models.CharField(max_length=255)
    password = EncryptedTextField()

    apiURL = models.CharField(max_length=255, default="https://managerapi.mosyle.com/v2")

    def process(self):
        login_response = requests.post(
            self.apiURL + "/login",
            json = {
                'email' : self.username,
                'password' : self.password,
                'accessToken' : self.accessToken
            },
            headers = {
                'Content-Type' : 'application/json'
            }
        )

        if not login_response.ok:
            print("error: " + login_response.json()['error-description'])
            return

        # get bearer_token from authorization header
        bearer = login_response.headers['Authorization']

        def apiCall(self, options):
            # cycle through pages of devices
            return requests.post(
                self.apiURL + "/listdevices",
                headers = {
                    'Content-Type' : 'application/json',
                    'Authorization' : bearer
                },
                json = {
                    'accessToken' : self.accessToken,
                    'options' : options
                }
            ).json()

        def cyclePages(self, options):
            print("here")
            response = apiCall(self, options)

            # check for errors
            if 'error' in response:
                print("error: " + response['error-description'])
                return []

            devices = response['response']['devices']

            # check for more pages
            while int(response['response']['page_size']) * int(response['response']['page']) < int(response['response']['rows']):
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
