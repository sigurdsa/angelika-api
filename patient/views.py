from .models import Patient
from rest_framework import viewsets
from .serializers import PatientListSerializer, PatientDetailSerializer, CurrentPatientSerializer,\
    PatientGraphSeriesSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from api.permissions import IsHealthProfessional, IsPatient
from rest_framework.permissions import IsAuthenticated
from next_of_kin.models import NextOfKin
from motivation_text.models import MotivationText
from measurement.models import Measurement
from alarm.models import Alarm
from django.utils import timezone
from datetime import timedelta
from rest_framework.decorators import detail_route
from rest_framework.exceptions import ParseError
from threshold_value.models import ThresholdValue


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

        if 'next_of_kin' in request.DATA:
            next_of_kin_ids = []
            i = 0
            for next_of_kin_dict in request.DATA['next_of_kin']:
                if 'id' in next_of_kin_dict and next_of_kin_dict['id']:
                    next_of_kin_ids.append(next_of_kin_dict['id'])
                    NextOfKin.objects.filter(id=next_of_kin_dict['id']).update(
                        priority=i, **next_of_kin_dict)
                else:
                    new_next_of_kin = NextOfKin(patient_id=kwargs['pk'],
                                                priority=i, **next_of_kin_dict)
                    new_next_of_kin.save()
                    next_of_kin_ids.append(new_next_of_kin.id)
                i += 1

            num_next_of_kin = NextOfKin.objects.filter(patient__id=patient_id).count()
            if num_next_of_kin != len(request.DATA['next_of_kin']):
                for next_of_kin in NextOfKin.objects.filter(patient__id=patient_id):
                    if not next_of_kin.id in next_of_kin_ids:
                        next_of_kin.delete()

        if 'motivation_texts' in request.DATA:
            motivation_text_ids = []
            for motivation_text_dict in request.DATA['motivation_texts']:
                if 'time_created' in motivation_text_dict:
                    del motivation_text_dict['time_created']
                if 'id' in motivation_text_dict and motivation_text_dict['id']:
                    motivation_text_ids.append(motivation_text_dict['id'])
                    MotivationText.objects.filter(id=motivation_text_dict['id']).update(
                        **motivation_text_dict)
                else:
                    new_motivation_text = MotivationText(type='M', patient_id=kwargs['pk'],
                                                         **motivation_text_dict)
                    new_motivation_text.save()
                    motivation_text_ids.append(new_motivation_text.id)

            num_motivation_text = MotivationText.objects.filter(
                patient__id=patient_id, type='M').count()
            if num_motivation_text != len(request.DATA['motivation_texts']):
                for motivation_text in MotivationText.objects.filter(
                        patient__id=patient_id, type='M'):
                    if not motivation_text.id in motivation_text_ids:
                        motivation_text.delete()

        if 'information_texts' in request.DATA:
            information_text_ids = []
            for information_text_dict in request.DATA['information_texts']:
                if 'time_created' in information_text_dict:
                    del information_text_dict['time_created']
                if 'id' in information_text_dict and information_text_dict['id']:
                    information_text_ids.append(information_text_dict['id'])
                    MotivationText.objects.filter(id=information_text_dict['id']).update(
                        **information_text_dict)
                else:
                    new_information_text = MotivationText(type='I', patient_id=kwargs['pk'],
                                                          **information_text_dict)
                    new_information_text.save()
                    information_text_ids.append(new_information_text.id)

            num_information_text = MotivationText.objects.filter(
                patient__id=patient_id, type='I').count()
            if num_information_text != len(request.DATA['information_texts']):
                for information_text in MotivationText.objects.filter(
                        patient__id=patient_id, type='I'):
                    if not information_text.id in information_text_ids:
                        information_text.delete()

        def update_or_create_threshold_value(value, type, is_upper_threshold):
            existing_threshold_value = ThresholdValue.objects.filter(
                patient_id=patient_id,
                type=type,
                is_upper_threshold=is_upper_threshold
            ).last()

            if (existing_threshold_value and existing_threshold_value.value != value)\
                    or existing_threshold_value is None:
                ThresholdValue.objects.create(
                    value=value,
                    patient_id=patient_id,
                    type=type,
                    is_upper_threshold=is_upper_threshold
                )

        if 'o2_min' in request.DATA:
            update_or_create_threshold_value(request.DATA['o2_min'], 'O', False)

        if 'o2_max' in request.DATA:
            update_or_create_threshold_value(request.DATA['o2_max'], 'O', True)

        if 'pulse_min' in request.DATA:
            update_or_create_threshold_value(request.DATA['pulse_min'], 'P', False)

        if 'pulse_max' in request.DATA:
            update_or_create_threshold_value(request.DATA['pulse_max'], 'P', True)

        if 'temperature_min' in request.DATA:
            update_or_create_threshold_value(request.DATA['temperature_min'], 'T', False)

        if 'temperature_max' in request.DATA:
            update_or_create_threshold_value(request.DATA['temperature_max'], 'T', True)

        return self.update(request, *args, **kwargs)

    @detail_route()
    def graph_data(self, request, pk=None):
        type = self.request.QUERY_PARAMS.get('type', None)
        if type is None:
            raise ParseError(detail="Query string 'type' is not specified")
        if not type in ['A', 'O', 'P', 'T']:
            raise ParseError(detail="type must be one of the following values: 'A', 'O', 'P', 'T'")

        serializer = PatientGraphSeriesSerializer(
            instance=self.get_object(),
            context={
                'type': type,
                'min_time': timezone.now() - timedelta(days=365)
            }
        )
        return Response(serializer.data)


class CurrentPatient(APIView):
    """
    View for details about currently logged in patient
    """
    permission_classes = (IsAuthenticated, IsPatient,)

    def get(self, request, format=None):
        patient = request.user.patient
        serializer = CurrentPatientSerializer(instance=patient)
        return Response(serializer.data)


class CurrentPatientCallMeRequest(APIView):
    permission_classes = (IsAuthenticated, IsPatient,)

    def post(self, request, format=None):
        current_patient = self.request.user.patient

        num_already_requested = Measurement.objects.filter(
            patient=current_patient,
            type='C',  # CALL_ME_REQUEST
            time__gt=timezone.now() - timedelta(hours=1)
        ).count()

        if num_already_requested >= 1:
            return Response({'status': 'already_requested'})

        call_me_measurement = Measurement.objects.create(
            patient=current_patient,
            type='C',  # CALL_ME_REQUEST
            time=timezone.now()
        )

        Alarm.objects.create(
            measurement=call_me_measurement,
            time_created=call_me_measurement.time,
        )

        return Response({'status': 'ok'})
