from .models import Measurement
from rest_framework.exceptions import ParseError
from api.permissions import IsPatient, IsHub
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
from datetime import datetime
from patient.models import Patient
from patient.serializers import PatientGraphSeriesSerializer
from django.utils import timezone
from datetime import timedelta
from threshold_value.models import ThresholdValue
from pytz import UTC
from alarm.models import Alarm


class CurrentPatientMeasurements(APIView):
    permission_classes = (IsAuthenticated, IsPatient,)

    def get(self, request, format=None):
        type = self.request.QUERY_PARAMS.get('type', None)
        if type is None:
            raise ParseError(detail="Query string 'type' is not specified")
        if not type in ['A', 'O', 'P', 'T']:
            raise ParseError(detail="type must be one of the following values: 'A', 'O', 'P', 'T'")

        patient = request.user.patient
        if 'A' == type and not patient.activity_access:
            raise PermissionDenied()
        if 'O' == type and not patient.o2_access:
            raise PermissionDenied()
        if 'P' == type and not patient.pulse_access:
            raise PermissionDenied()
        if 'T' == type and not patient.temperature_access:
            raise PermissionDenied()

        serializer = PatientGraphSeriesSerializer(
            instance=patient,
            context={
                'type': type,
                'exclude_measurement_alarms': True,
                'min_time': timezone.now() - timedelta(days=7)
            }
        )
        return Response(serializer.data)


class PostMeasurements(APIView):
    permission_classes = (IsAuthenticated, IsHub, )

    def __init__(self):
        # Map hub-type --> model type
        self.allowed_types = {"heart_rate": 'P', "spo2": 'O', "steps": 'A'}  # Maps value to model type

        # Map hub-unit --> model unit
        self.allowed_units = {"bpm": 'B', "percent": 'E', 'steps': 'S', "m": 'M', 'kcal': 'K', 's': 'S'}

        # Filter out all activities but steps
        self.ignored_types = ["elevation", "calories", "soft", "intense", "moderate", "distance"]

    def post(self, request, format=None):
        hub_id = request.DATA.get("Observation").get("hub_id")

        try:
            patient = Patient.objects.get(hub__username=hub_id)
        except Patient.DoesNotExist:
            raise ParseError(detail='hub_id could not be mapped to patient')

        num_measurements_created = 0
        num_alarms_created = 0

        for measurement in request.DATA.get("Measurements"):
            date = measurement.get("date")
            m_type = measurement.get("type")
            unit = measurement.get("unit")
            value = measurement.get("value")

            if m_type in self.ignored_types:
                continue

            m_type = self.allowed_types[m_type]
            unit = self.allowed_units[unit]

            # Convert measurement datetime to timezone-aware format
            time = datetime.utcfromtimestamp(date).replace(tzinfo=UTC)

            measurement = None
            if m_type == 'A':
                measurement = Measurement.objects.filter(
                    patient=patient,
                    time=time,
                    type=m_type,
                    unit=unit
                ).first()

            if measurement:  # update existing measurement instead of creating a new one
                if measurement.value < value:
                    measurement.value = value
                    measurement.save()
            else:
                measurement = Measurement.objects.create(
                    patient=patient,
                    time=time,
                    type=m_type,
                    value=value,
                    unit=unit
                )
                num_measurements_created += 1

            if self.create_alert_if_abnormal(measurement):
                num_alarms_created += 1

        status_code = status.HTTP_200_OK
        if num_measurements_created > 0 or num_alarms_created > 0:
            status_code = status.HTTP_201_CREATED

        return Response(
            {
                'num_measurements_created': num_measurements_created,
                'num_alerts_created': num_alarms_created
            },
            status=status_code
        )

    def create_alert_if_abnormal(self, measurement):
        if not measurement.type in ['O', 'P', 'T']:
            return None

        upper_threshold_value = ThresholdValue.objects.filter(
            patient=measurement.patient,
            type=measurement.type,
            is_upper_threshold=True,
            time__lte=measurement.time
        ).last()

        too_high = upper_threshold_value and measurement.value > upper_threshold_value.value

        if measurement.type == 'O' and too_high:
            return None  # Don't create an alarm when O2 is too high

        lower_threshold_value = ThresholdValue.objects.filter(
            patient=measurement.patient,
            type=measurement.type,
            is_upper_threshold=False,
            time__lte=measurement.time
        ).last()

        too_low = lower_threshold_value and measurement.value < lower_threshold_value.value

        if too_low or too_high:
            # check if there's already an untreated alarm for this incident
            recent_untreated_alarm = Alarm.objects.filter(
                measurement__patient=measurement.patient,
                measurement__type=measurement.type,
                is_treated=False
            ).first()
            if not recent_untreated_alarm:
                return Alarm.objects.create(measurement=measurement)

        return None
