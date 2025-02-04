from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from core.models import User
from freeradius.models import Device, CsvImporter, PostAuthLog
from integrations.models import MosyleIntegration
from bootstrap_modal_forms.forms import BSModalModelForm

class AuthForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username','password']
    def __init__(self, *args, **kwargs):
        super(AuthForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E-mail Address'})
        self.fields['username'].label = False
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password'})
        self.fields['password'].label = False


class DeviceForm(BSModalModelForm):

    class Meta:
        model = Device
        fields = (
            'mac',
            'hostname',
            'description',
        )

        widgets = {
            'mac': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ac:de:48:01:2e:a0'}),
            'hostname': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control h-25', 'rows': '4', 'placeholder': 'User A Desktop Wi-Fi Add-on card'}),
        }

        labels = {
            'mac': 'MAC Address',
        }

class CsvImportForm(BSModalModelForm):

    class Meta:
        model = CsvImporter
        fields = (
            'csvfile',
            'mac_header',
            'hostname_header',
            'description_header',
            'overwrite',
        )

        widgets = {
            'mac_header': forms.TextInput(attrs={'class': 'form-control'}),
            'hostname_header': forms.TextInput(attrs={'class': 'form-control'}),
            'description_header': forms.TextInput(attrs={'class': 'form-control h-25'}),
        }

        labels = {
            'csvfile': 'CSV File',
            'mac_header': 'MAC Address Header',
            'hostname_header': 'Hostname Header (Optional)',
            'description_header': 'Description Header (Optional)',
            'overwrite': "Overwrite existing hostname & description?",
        }

class PostAuthLogROForm(BSModalModelForm):

    def __init__(self,disable_fields=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].disabled = True
        self.fields['packet_type'].disabled = True
        self.fields['called_station_id'].disabled = True
        self.fields['calling_station_id'].disabled = True
        self.fields['operator_name'].disabled = True
        self.fields['datetime'].disabled = True
        self.fields['reject_cause'].disabled = True
        self.fields['vlan_id'].disabled = True
        self.fields['trusted_device'].disabled = True

    class Meta:
        model = PostAuthLog
        fields = [
            'username',
            'packet_type',
            'called_station_id',
            'calling_station_id',
            'operator_name',
            'datetime',
            'reject_cause',
            'vlan_id',
            'trusted_device',
        ]

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'packet_type': forms.TextInput(attrs={'class': 'form-control'}),
            'called_station_id': forms.TextInput(attrs={'class': 'form-control'}),
            'calling_station_id': forms.TextInput(attrs={'class': 'form-control'}),
            'operator_name': forms.TextInput(attrs={'class': 'form-control'}),
            'datetime': forms.TextInput(attrs={'class': 'form-control'}),
            'reject_cause': forms.Textarea(attrs={'class': 'form-control h-25', 'rows': '4'}),
            'vlan_id': forms.TextInput(attrs={'class': 'form-control'}),
            #'trusted_device': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }

class MosyleForm(BSModalModelForm):

    class Meta:
        model = MosyleIntegration
        fields = (
            'name',
            'description',
            'username',
            'password',
            'accessToken',
        )

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control h-25', 'rows': '4', 'placeholder': 'District A Mosyle setup'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'accessToken': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'mac': 'MAC Address',
        }
