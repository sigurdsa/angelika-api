from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from alarm import views as alarm_views
from patient import views as patient_views
from measurement import views as measurement_views

router = routers.DefaultRouter()
router.register(r'alarms', alarm_views.AlarmViewSet, base_name='Alarms')
router.register(r'patients', patient_views.PatientViewSet, base_name='Patients')

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', 'token_auth.views.custom_obtain_auth_token'),
    url(r'^current-patient/call_me/', patient_views.CurrentPatientCallMeRequest.as_view()),
    url(r'^current-patient/graph_data/', measurement_views.CurrentPatientMeasurements.as_view()),
    url(r'^current-patient/', patient_views.CurrentPatient.as_view()),
    url(r'^post-measurements/', measurement_views.PostMeasurements.as_view()),
)
