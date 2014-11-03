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

    def post(self, request, format=None):

        hub_id = request.DATA.get("Observation").get("hub_id")

        patient = Patient.objects.get(hub__username=hub_id)

        if patient:
            patient_id = patient.id
        else:
            return Response({"hub_id could not be mapped to patient": -1}, status=status.HTTP_400_BAD_REQUEST)

        count = 0  # How many measurements gets created?

        for measurement in request.DATA.get("Measurements"):

            date = measurement.get("date")
            m_type = measurement.get("type")  # only steps should be used for now
            unit = measurement.get("unit")
            value = measurement.get("value")

            # Filter out all activities but steps
            ignored_types = ["elevation", "calories", "soft", "intense", "moderate", "distance"]
            if m_type in ignored_types:
                continue

            count += 1

            # Map hub-type --> model type
            allowed_types = {"heart_rate": 'P', "spo2": 'O', "steps": 'A'}  # Maps value to model type
            m_type = allowed_types[m_type]

            # Map hub-unit --> model unit
            allowed_units = {"bpm": 'B', "percent": 'E', 'steps': 'S', "m": 'M', 'kcal': 'K', 's': 'S'}
            unit = allowed_units[unit]

            # Convert time format
            time = datetime.utcfromtimestamp(date)

            # Time must be timezone-aware
            tz_aware_time = time.replace(tzinfo=pytz.UTC)

            Measurement.objects.create(
                patient_id=patient_id,
                time=tz_aware_time,
                type=m_type,
                value=value,
                unit=unit
            )

        return Response({'num_measurements': count}, status=status.HTTP_201_CREATED)
