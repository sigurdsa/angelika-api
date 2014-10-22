from .models import Patient
from rest_framework import viewsets
from .serializers import PatientListSerializer, PatientDetailSerializer, CurrentPatientSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from api.permissions import IsHealthProfessional, IsPatient
from rest_framework.permissions import IsAuthenticated


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    permission_classes = (IsAuthenticated, IsHealthProfessional,)

    def get_serializer_class(self):
        if self.action == 'list':
            return PatientListSerializer
        else:
            return PatientDetailSerializer


class CurrentPatient(APIView):
    """
    View for details about currently logged in patient
    """
    permission_classes = (IsAuthenticated, IsPatient,)

    def get(self, request, format=None):
        patient = request.user.patient
        exclude_fields = []
        if not patient.o2_access:
            exclude_fields += ['o2_min', 'o2_max']
        if not patient.pulse_access:
            exclude_fields += ['pulse_min', 'pulse_max']
        if not patient.temperature_access:
            exclude_fields += ['temperature_min', 'temperature_max']
        serializer = CurrentPatientSerializer(instance=patient, exclude=exclude_fields)
        return Response(serializer.data)
