from django.conf.urls import url, include
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from rest_framework import routers
from . import views
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'devices', views.DeviceViewSet, basename='devices')
router.register(r'imports/csv', views.CsvImporterViewSet)
#router.register(r'vuln/details', views.VulnDetailsViewSet)
#router.register(r'vuln', views.VulnViewSet, basename='Vulnerability')
#router.register(r'imports', views.ImportViewSet)
#router.register(r'mailboxes', views.MailboxViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
