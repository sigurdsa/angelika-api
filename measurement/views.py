from .models import Measurement
from rest_framework import viewsets
from graph.serializers import MeasurementGraphSerializer
from rest_framework.exceptions import ParseError
from api.permissions import IsPatient
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response


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
