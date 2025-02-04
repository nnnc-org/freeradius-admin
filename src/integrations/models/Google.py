from . import BaseIntegration

from django.db import models
from fernet_fields import EncryptedTextField

import json, datetime
from operator import itemgetter


class GoogleIntegraion(BaseIntegration):
    username = models.CharField(max_length=255)
    service_account = EncryptedTextField()

    def process(self):

        import google.auth
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
        from google.oauth2.service_account import Credentials

        SCOPES = ['https://www.googleapis.com/auth/admin.directory.device.chromeos.readonly']

        SERVICE_ACCOUNT_INFO = json.loads(self.service_account)
        ADMIN_USER = self.username

        # Authenticate using the service account
        def authenticate_service_account():
            creds = Credentials.from_service_account_info(
                SERVICE_ACCOUNT_INFO,
                scopes=SCOPES,
                subject=ADMIN_USER  # This impersonates an admin user
            )

            # Refresh the credentials if they are expired
            if creds.expired and creds.refresh_token:
                creds.refresh(Request())

            return creds

        # Build the Directory API service
        def build_service():
            creds = authenticate_service_account()
            service = build('admin', 'directory_v1', credentials=creds)
            return service

        # Fetch Chromebook MAC addresses
        def get_chromebook_mac_addresses():
            service = build_service()

            # List Chrome devices
            devices = []
            page_token = None
            while True:
                results = service.chromeosdevices().list(
                    customerId='my_customer',  # This is your domain's customer ID (use 'my_customer' for most cases)
                    pageToken=page_token
                ).execute()

                for device in results.get('chromeosdevices', []):
                    mac_address = device.get('macAddress')
                    if mac_address:
                        devices.append({
                            'serial_number': device.get('serialNumber'),
                            'mac_address': mac_address,
                            'asset_tag': device.get('annotatedAssetId'),
                            'model': device.get('model'),
                            'last_sync': device.get('lastSync'),
                        })

                page_token = results.get('nextPageToken')
                if not page_token:
                    break

            return devices

        devices = get_chromebook_mac_addresses()
        for device in devices:
            if device['last_sync'] > datetime.datetime.now() - datetime.timedelta(days=30):
                self.add_device_raw(
                    device['mac_address'],
                    device['serial_number'],
                    " ".join([device['model'], device['asset_tag']])
                )

        for d in self.devices.all():
            if d.mac not in list(map(itemgetter('mac_address'), devices)):
                self.remove_device(d.mac)
