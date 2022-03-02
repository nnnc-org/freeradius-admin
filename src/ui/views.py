from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, View, ListView, DetailView
from django.views.generic.edit import UpdateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView

from .forms import DeviceForm, CsvImportForm
from freeradius.models import Device, CsvImporter


@method_decorator(login_required, name='dispatch')
class DashboardView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "radius/dashboard.html")


@method_decorator(login_required, name='dispatch')
class DeviceView(ListView):
    template_name = "radius/devices.html"
    model = Device
    context_object_name = "devices"
    paginate_by = 50

    def get_ordering(self):
        ordering = self.request.GET.get('order_by', '-created_at')
        return ordering

@method_decorator(login_required, name='dispatch')
class CsvImportView(ListView):
    template_name = "radius/csv_imports.html"
    model = CsvImporter
    context_object_name = "imports"
    paginate_by = 50

    def get_ordering(self):
        ordering = self.request.GET.get('order_by', '-created_at')
        return ordering

@method_decorator(login_required, name='dispatch')
class CsvImportCreateView(BSModalCreateView):
    template_name = 'radius/add_csvimport.html'
    form_class = CsvImportForm
    success_message = 'Success: Import was created.'
    success_url = reverse_lazy('devices')

@method_decorator(login_required, name='dispatch')
class DeviceCreateView(BSModalCreateView):
    template_name = 'radius/add_device.html'
    form_class = DeviceForm
    success_message = 'Success: Device was created.'
    success_url = reverse_lazy('devices')


@method_decorator(login_required, name='dispatch')
class DeviceEditView(BSModalUpdateView):
    template_name = 'radius/add_device.html'
    form_class = DeviceForm
    model = Device
    success_message = 'Success: Device was updated.'
    success_url = reverse_lazy('devices')

