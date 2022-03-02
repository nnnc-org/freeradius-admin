from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from core.models import User
from freeradius.models import Device, CsvImporter
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
        }