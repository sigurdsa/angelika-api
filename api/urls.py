from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from alarm import views as alarm_views
from patient import views as patient_views

router = routers.DefaultRouter()
router.register(r'alarms', alarm_views.AlarmViewSet)
router.register(r'patients',patient_views.PatientViewSet)

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token'),
)
