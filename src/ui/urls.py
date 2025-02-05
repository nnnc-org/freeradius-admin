from django.conf.urls import url, include
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views
from .forms import AuthForm

urlpatterns = [
    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name = 'auth/login.html', authentication_form=AuthForm), name='login'),
    path('logout', auth_views.LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),

    # user views
    path('', views.DashboardView.as_view(), name='home'),
    path('log/view/<pk>', views.PostAuthLogReadOnlyEditView.as_view(), name='log_view'),
    path('devices/', views.DeviceView.as_view(), name='devices'),
    path('devices/add/', views.DeviceCreateView.as_view(), name='device_add'),
    path('devices/edit/<pk>', views.DeviceEditView.as_view(), name='device_edit'),
    #path('devices/delete/<pk>', views.DeviceEditView.as_view(), name='device_edit'),
    path('imports/csv/', views.CsvImportView.as_view(), name='csvimports'),
    path('imports/csv/add/', views.CsvImportCreateView.as_view(), name='csvimport_add'),
    #path('imports/csv/edit/<pk>', views.CsvImportEditView.as_view(), name='csvimport_edit'),
    #path('imports/csv/process/<pk>', views.CsvImportProcessView.as_view(), name='csvimport_process'),
    #path('imports/csv/delete/<pk>', views.CsvImportProcessView.as_view(), name='csvimport_process'),

    path('integrations/', views.IntegrationList.as_view(), name='integrations'),
    path('integrations/mosyle/add/', views.MosyleCreateView.as_view(), name='mosyle_add'),
    path('integrations/mosyle/edit/<pk>', views.MosyleEditView.as_view(), name='mosyle_edit'),
    path('integrations/google/add/', views.GoogleCreateView.as_view(), name='google_add'),
    path('integrations/google/edit/<pk>', views.GoogleEditView.as_view(), name='google_edit'),

    # settings
    #path('settings/', views.SettingsView.as_view(), name='settings'),
]
