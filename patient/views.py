from .models import Patient
from rest_framework import viewsets
from .serializers import PatientListSerializer, PatientDetailSerializer, CurrentPatientSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from api.permissions import IsHealthProfessional, IsPatient
from rest_framework.permissions import IsAuthenticated
from next_of_kin.models import NextOfKin


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    permission_classes = (IsAuthenticated, IsHealthProfessional,)

    def get_serializer_class(self):
        if self.action == 'list':
            return PatientListSerializer
        else:
            return PatientDetailSerializer

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        patient_id = kwargs['pk']

        next_of_kin_ids = []
        for next_of_kin_dict in request.DATA['next_of_kin']:
            if 'id' in next_of_kin_dict and next_of_kin_dict['id']:
                next_of_kin_ids.append(next_of_kin_dict['id'])
                NextOfKin.objects.filter(id=next_of_kin_dict['id']).update(**next_of_kin_dict)
            else:
                new_next_of_kin = NextOfKin(patient_id=kwargs['pk'], **next_of_kin_dict)
                new_next_of_kin.save()
                next_of_kin_ids.append(new_next_of_kin.id)

        num_next_of_kin = NextOfKin.objects.filter(patient__id=patient_id).count()
        if num_next_of_kin != len(request.DATA['next_of_kin']):
            for next_of_kin in NextOfKin.objects.filter(patient__id=patient_id):
                if not next_of_kin.id in next_of_kin_ids:
                    next_of_kin.delete()

        return self.update(request, *args, **kwargs)


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
