from datetime import datetime, timedelta

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, View, ListView, DetailView
from django.views.generic.edit import UpdateView, FormView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView

from .forms import DeviceForm, CsvImportForm, PostAuthLogROForm, MosyleForm
from freeradius.models import Device, CsvImporter, PostAuthLog
from integrations.models import MosyleIntegration


@method_decorator(login_required, name='dispatch')
class DashboardView(ListView):
    template_name = "radius/dashboard.html"
    model = PostAuthLog
    context_object_name = "logs"
    paginate_by = 12
    ordering = ['-created_at']

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = PostAuthLog.objects.order_by('-created_at').filter(created_at__gte=datetime.now()-timedelta(days=7))
        if query:
            object_list = PostAuthLog.objects.order_by('-created_at').filter(created_at__gte=datetime.now()-timedelta(days=7)).filter(
                Q(calling_station_id__icontains=query) | Q(created_at__icontains=query) | Q(packet_type__icontains=query) | Q(username__icontains=query)
            )
        return object_list

    def get_context_data(self,**kwargs):
        context = super(DashboardView,self).get_context_data(**kwargs)
        context['success_logins']=PostAuthLog.objects.order_by('-created_at').filter(created_at__gte=datetime.now()-timedelta(days=7), packet_type="Access-Accept").count()
        context['failed_logins']=PostAuthLog.objects.order_by('-created_at').filter(created_at__gte=datetime.now()-timedelta(days=7), packet_type="Access-Reject").count()
        context['trusted_devices']=PostAuthLog.objects.order_by('-created_at').filter(created_at__gte=datetime.now()-timedelta(days=7), packet_type="Access-Accept", trusted_device=True).count()
        context['personal_devices']=PostAuthLog.objects.order_by('-created_at').filter(created_at__gte=datetime.now()-timedelta(days=7), packet_type="Access-Accept", trusted_device=False).count()

        return context

@method_decorator(login_required, name='dispatch')
class DeviceView(ListView):
    template_name = "radius/devices.html"
    model = Device
    context_object_name = "devices"
    paginate_by = 50

    def get_queryset(self):
        query = self.request.GET.get('q')
        ordering = self.request.GET.get('order_by', '-created_at')
        object_list = Device.objects.order_by(ordering).all()
        if query:
            object_list = Device.objects.order_by(ordering).filter(
                Q(mac__icontains=query) | Q(hostname__icontains=query) | Q(description__icontains=query)
            )
        return object_list

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
    success_message = 'Import was created.'
    success_url = reverse_lazy('csvimports')

@method_decorator(login_required, name='dispatch')
class DeviceCreateView(BSModalCreateView):
    template_name = 'radius/add_device.html'
    form_class = DeviceForm
    success_message = 'Device was created.'
    success_url = reverse_lazy('devices')


@method_decorator(login_required, name='dispatch')
class DeviceEditView(BSModalUpdateView):
    template_name = 'radius/add_device.html'
    form_class = DeviceForm
    model = Device
    success_message = 'Device was updated.'
    success_url = reverse_lazy('devices')

@method_decorator(login_required, name='dispatch')
class PostAuthLogReadOnlyEditView(BSModalUpdateView):
    template_name = 'radius/view_log.html'
    form_class = PostAuthLogROForm
    model = PostAuthLog
    success_url = reverse_lazy('home')

@method_decorator(login_required, name='dispatch')
class IntegrationList(ListView):
    template_name = "integrations/list.html"
    model = MosyleIntegration
    context_object_name = "integrations"
    paginate_by = 10

@method_decorator(login_required, name='dispatch')
class MosyleCreateView(BSModalCreateView):
    template_name = 'integrations/add_mosyle.html'
    form_class = MosyleForm
    success_message = 'Integration was created.'
    success_url = reverse_lazy('integrations')
