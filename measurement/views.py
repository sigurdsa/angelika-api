from .models import Measurement
from rest_framework import viewsets
from .serializers import MeasurementGraphSerializer
from rest_framework.exceptions import ParseError
from api.permissions import IsHealthProfessional, IsPatient
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
from datetime import datetime
from patient.models import Patient


class MeasurementViewSet(viewsets.ModelViewSet):
    """
    API endpoint that shows measurement from one patient
    """
    serializer_class = MeasurementGraphSerializer
    permission_classes = (IsAuthenticated, IsHealthProfessional,)

    def get_queryset(self):
        patient_id = self.request.QUERY_PARAMS.get('patient_id', None)
        if patient_id is None:
            raise ParseError(detail="Query string 'patient_id' not specified")
        if not patient_id.isdigit():
            raise ParseError(detail="patient_id is not numeric")
        type = self.request.QUERY_PARAMS.get('type', None)
        if type is None:
            raise ParseError(detail="Query string 'type' is not specified")
        if not type in ['A', 'O', 'P', 'T']:
            raise ParseError(detail="type must be one of the following values: 'A', 'O', 'P', 'T'")

        queryset = Measurement.objects.filter(patient__id=patient_id, type=type)
        return queryset


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

        queryset = Measurement.objects.filter(patient__id=patient.id, type=type)
        serializer = MeasurementGraphSerializer(queryset, many=True)
        return Response(serializer.data)

class PostMeasurements(APIView):
    permission_classes = () # TODO: Fix permissions, for example (IsAuthenticated, IsHub,)

    def post(self, request, format=None):
        print request.DATA
        print len(request.DATA)

        print ""

        print "Observation: ", request.DATA.get("Observation")

        print "HUB_ID: ", request.DATA.get("Observation").get("hub_id")
        hub_id = request.DATA.get("Observation").get("hub_id")

        # print "Measurements: ", request.DATA.get("Measurements")
        print "Measurements: "
        print request.DATA.get("Measurements")

        count = 0 # just to know how many measurements gets created

        for measurement in request.DATA.get("Measurements"):

            date = measurement.get("date")
            type = measurement.get("type") # only steps should be used for now, check this
            unit = measurement.get("unit")
            value = measurement.get("value")

            # Filter out all activities but steps
            ignored_types = ["elevation", "calories", "soft", "intense", "moderate", "distance"]
            if type in ignored_types:
                continue

            count += 1


            # Map hub-type --> model type
            allowed_types = {"heart_rate" : 'P', "spo2": 'O', "steps": 'A'} # Maps value to model type
            type = allowed_types[type]

            # Map hub-unit --> model unit
            allowed_units = {"bpm": 'B', "percent" : 'E', 'steps': 'S', "m": 'M', 'kcal': 'K', 's': 'S'}
            unit = allowed_units[unit]

            # Convert time format
            time = datetime.utcfromtimestamp(date)

            # TODO map hub id to patient id!!!!
            patient_id = Patient.objects.all().first().id

            print "Will create measurement object with Time: ", time, "Type: ", type, "Value: ", value, "Unit: ", unit, " from hub: ", hub_id


            Measurement.objects.create(
                patient_id=patient_id,
                time=time,
                type=type,
                value=value,
                unit=unit
            )

            print "Posted..."
            print "-----------------------------"
        print "Measurements created: ", count


        return Response({'WOHOO': True})
