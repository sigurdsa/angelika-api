from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from alarm import views as alarm_views
from patient import views as patient_views
from measurement import views as measurement_views
from motivation_text import views as motivation_views
from next_of_kin import views as next_of_kin_views

router = routers.DefaultRouter()
router.register(r'alarms', alarm_views.AlarmViewSet)
router.register(r'patients', patient_views.PatientViewSet, base_name='Patients')
router.register(r'measurements', measurement_views.MeasurementViewSet, base_name='Measurements')
router.register(r'motivation_text', motivation_views.MotivationTextViewSet)
router.register(r'next_of_kin', next_of_kin_views.NextOfKinViewSet)

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', 'token_auth.views.custom_obtain_auth_token'),
    url(r'^current-patient/', patient_views.CurrentPatient.as_view()),
    url(r'^current-patient-measurements/', measurement_views.CurrentPatientMeasurements.as_view()),
)
