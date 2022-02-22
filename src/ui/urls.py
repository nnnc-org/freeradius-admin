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
    path('devices/', views.DeviceView.as_view(), name='devices'),
    path('devices/add/', views.DeviceCreateView.as_view(), name='device_add'),
    path('devices/edit/<pk>', views.DeviceEditView.as_view(), name='device_edit'),

    # settings
    #path('settings/', views.SettingsView.as_view(), name='settings'),
]
