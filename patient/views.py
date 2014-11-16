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
from django.contrib.auth.models import User, Group
from rest_framework import status
from .helpers import generate_username
from .helpers import get_sound_filename
from base64 import b64decode
from django.core.files.uploadedfile import SimpleUploadedFile


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    permission_classes = (IsAuthenticated, IsHealthProfessional,)

    def get_serializer_class(self):
        if self.action == 'list':
            return PatientListSerializer
        else:
            return PatientDetailSerializer

    def create(self, request, *args, **kwargs):
        patient_data = request.DATA

        is_duplicate = Patient.objects.filter(
            national_identification_number=patient_data['national_identification_number']
        ).exists()
        if is_duplicate:
            return Response({'error': 'duplicate_national_identification_number'}, status=status.HTTP_409_CONFLICT)

        user_data = patient_data.pop('user', None)
        if user_data is None:
            raise ParseError(detail='User is not specified')
        next_of_kin_data = patient_data.pop('next_of_kin', None)
        motivation_text_data = patient_data.pop('motivation_texts', None)
        information_text_data = patient_data.pop('information_texts', None)
        o2_min_data = patient_data.pop('o2_min', None)
        o2_max_data = patient_data.pop('o2_max', None)
        pulse_min_data = patient_data.pop('pulse_min', None)
        pulse_max_data = patient_data.pop('pulse_max', None)
        temperature_min_data = patient_data.pop('temperature_min', None)
        temperature_max_data = patient_data.pop('temperature_max', None)

        username = generate_username(
            user_data['first_name'],
            user_data['last_name'],
            patient_data['national_identification_number'][4:6]
        )
        password = "perper"  # TODO: do not hard code this
        patient_user = User.objects.create(username=username, password=password, **user_data)
        patient_group = Group.objects.get(name='patients')
        patient_user.groups.add(patient_group)

        patient = Patient.objects.create(
            user=patient_user,
            **patient_data
        )

        if next_of_kin_data and len(next_of_kin_data) > 0:
            for i in range(len(next_of_kin_data)):
                next_of_kin_dict = next_of_kin_data[i]
                NextOfKin.objects.create(priority=i, patient=patient, **next_of_kin_dict)

        if motivation_text_data and len(motivation_text_data) > 0:
            for i in range(len(motivation_text_data)):
                motivation_text_dict = motivation_text_data[i]
                if 'sound' in motivation_text_dict:
                    sound = motivation_text_dict['sound']
                    if sound.get('is_updated', False):
                        mp3_filename = get_sound_filename()
                        mp3_file = SimpleUploadedFile(mp3_filename, b64decode(sound['base64']))
                        motivation_text_dict['sound'] = mp3_file
                MotivationText.objects.create(type='M', patient=patient, **motivation_text_dict)

        if information_text_data and len(information_text_data) > 0:
            for i in range(len(information_text_data)):
                information_text_dict = information_text_data[i]
                MotivationText.objects.create(type='I', patient=patient, **information_text_dict)

        def create_threshold_value(value, type, is_upper_threshold):
            ThresholdValue.objects.create(
                value=value,
                patient=patient,
                type=type,
                is_upper_threshold=is_upper_threshold
            )

        if o2_min_data:
            create_threshold_value(o2_min_data, 'O', False)
        if o2_max_data:
            create_threshold_value(o2_max_data, 'O', True)
        if pulse_min_data:
            create_threshold_value(pulse_min_data, 'P', False)
        if pulse_max_data:
            create_threshold_value(pulse_max_data, 'P', True)
        if temperature_min_data:
            create_threshold_value(temperature_min_data, 'T', False)
        if temperature_max_data:
            create_threshold_value(temperature_max_data, 'T', True)

        serializer = PatientDetailSerializer(instance=patient, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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
                if 'sound' in motivation_text_dict:
                    sound = motivation_text_dict.pop('sound')
                    if sound.get('is_updated', False):
                        mp3_filename = get_sound_filename()
                        mp3_file = SimpleUploadedFile(mp3_filename, b64decode(sound['base64']))
                        motivation_text_dict['sound'] = mp3_file
                if 'id' in motivation_text_dict and motivation_text_dict['id']:
                    motivation_text_ids.append(motivation_text_dict['id'])
                    motivation_text = MotivationText.objects.get(id=motivation_text_dict['id'])
                    if 'sound' in motivation_text_dict:
                        motivation_text.sound = motivation_text_dict['sound']
                    if 'text' in motivation_text_dict:
                        motivation_text.text = motivation_text_dict['text']
                    motivation_text.save()
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
            time__gt=timezone.now() - timedelta(minutes=5)
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
