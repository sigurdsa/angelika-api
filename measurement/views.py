from .models import Measurement
from rest_framework import viewsets
from .serializers import MeasurementGraphSerializer
from rest_framework.exceptions import ParseError


class MeasurementViewSet(viewsets.ModelViewSet):
    """
    API endpoint that shows measurement from one patient
    """
    serializer_class = MeasurementGraphSerializer

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
