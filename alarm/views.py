from .models import Alarm
from rest_framework import viewsets
from .serializers import AlarmSerializer, PatientAlarmSerializer
from api.permissions import IsHealthProfessional
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError


class AlarmViewSet(viewsets.ModelViewSet):
    """
    API endpoint that shows all alarms
    """
    permission_classes = (IsAuthenticated, IsHealthProfessional,)

    def get_serializer_class(self):
        patient_id = self.request.QUERY_PARAMS.get('patient_id', None)
        if patient_id is None:
            return AlarmSerializer
        else:
            return PatientAlarmSerializer

    def get_queryset(self):
        patient_id = self.request.QUERY_PARAMS.get('patient_id', None)
        if patient_id is None:
            return Alarm.objects.all()
        if not patient_id.isdigit():
            raise ParseError(detail="patient_id is not numeric")

        return Alarm.objects.filter(measurement__patient_id=patient_id)
