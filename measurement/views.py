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

import pytz


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

        num_measurements_created = 0  # How many measurements gets created?

        for measurement in request.DATA.get("Measurements"):
            date = measurement.get("date")
            m_type = measurement.get("type")
            unit = measurement.get("unit")
            value = measurement.get("value")

            if m_type in self.ignored_types:
                continue

            num_measurements_created += 1
            m_type = self.allowed_types[m_type]
            unit = self.allowed_units[unit]

            # Convert measurement datetime to timezone-aware format
            time = datetime.utcfromtimestamp(date)
            tz_aware_time = time.replace(tzinfo=pytz.UTC)

            Measurement.objects.create(
                patient=patient,
                time=tz_aware_time,
                type=m_type,
                value=value,
                unit=unit
            )

        return Response({'num_measurements': num_measurements_created}, status=status.HTTP_201_CREATED)
