from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from alarm import views as alarm_views
from patient.views import PatientViewSet
from measurement import views as measurement_views

router = routers.DefaultRouter()
router.register(r'alarms', alarm_views.AlarmViewSet)
router.register(r'patients',PatientViewSet, base_name='Patients')
router.register(r'measurements',measurement_views.MeasurementViewSet, base_name='Measurements')

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token'),
)
