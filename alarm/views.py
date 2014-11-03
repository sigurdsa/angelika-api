from .models import Alarm
from rest_framework import viewsets
from .serializers import AlarmSerializer, PatientAlarmSerializer
from api.permissions import IsHealthProfessional
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from motivation_text.models import MotivationText
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

    @detail_route(methods=['post'])
    def handle(self, request, pk=None):
        try:
            alarm_dict = request.DATA['alarm']
            motivation_text = request.DATA['motivation_text']

            alarm = self.get_object()
            alarm.is_treated = alarm_dict['is_treated']
            alarm.treated_text = alarm_dict['treated_text']
            alarm.save()

            if motivation_text:
                MotivationText.objects.create(
                    patient=alarm.measurement.patient,
                    text=motivation_text
                )

            serializer = PatientAlarmSerializer(instance=alarm)
            return Response(serializer.data)

        except KeyError:
            raise ParseError()

