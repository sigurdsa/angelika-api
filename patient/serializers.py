from django.contrib.auth.models import User
from .models import Patient
from rest_framework import serializers
import datetime
from next_of_kin.models import NextOfKin
from next_of_kin.serializers import NextOfKinSerializer
from motivation_text.models import MotivationText
from motivation_text.serializers import MotivationTextSerializer
from measurement.models import Measurement
from graph.serializers import MeasurementGraphSeriesSerializer, ThresholdValueGraphSeriesSerializer
from threshold_value.models import ThresholdValue
from alarm.models import Alarm


class SimpleUserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField('get_full_name')

    class Meta:
        model = User
        fields = ['full_name', ]

    def get_full_name(self, obj):
        return obj.get_full_name()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class SimplePatientSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()

    class Meta:
        model = Patient
        fields = ('id', 'user')


class PatientListSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()
    birth_date = serializers.SerializerMethodField('get_birth_date')
    age = serializers.SerializerMethodField('get_age')

    def get_birth_date(self, obj):
        return obj.national_identification_number[0:2] + "." \
            + obj.national_identification_number[2:4] + "." \
            + obj.national_identification_number[4:6]

    def get_age(self, obj):
        today = datetime.datetime.today()
        ddmm = obj.national_identification_number[0:4]
        yyyy = "20" + obj.national_identification_number[4:6]
        if int(yyyy) >= today.year:
            yyyy = str(int(yyyy) - 100)
        try:
            birth_date = datetime.datetime.strptime(ddmm + yyyy, "%d%m%Y")
            diff = today - birth_date
            num_years = int(diff.days / 365.2425)  # rough estimate, can be wrong in some edge cases
            return num_years
        except ValueError:
            return None

    class Meta:
        model = Patient
        fields = [
            'id',
            'user',
            'birth_date',
            'age',
            'national_identification_number',
            'phone_number'
        ]


class PatientDetailSerializer(PatientListSerializer):
    user = UserSerializer()
    next_of_kin = serializers.SerializerMethodField('get_next_of_kin')
    motivation_texts = serializers.SerializerMethodField('get_motivation_texts')
    information_texts = serializers.SerializerMethodField('get_information_texts')
    o2_min = serializers.SerializerMethodField('get_o2_min')
    o2_max = serializers.SerializerMethodField('get_o2_max')
    pulse_min = serializers.SerializerMethodField('get_pulse_min')
    pulse_max = serializers.SerializerMethodField('get_pulse_max')
    temperature_min = serializers.SerializerMethodField('get_temperature_min')
    temperature_max = serializers.SerializerMethodField('get_temperature_max')

    def get_next_of_kin(self, obj):
        next_of_kin = NextOfKin.objects.filter(patient__id=obj.id)
        serializer = NextOfKinSerializer(next_of_kin, many=True, context=self.context)
        return serializer.data

    def get_motivation_texts(self, obj):
        motivation_texts = MotivationText.objects.filter(patient__id=obj.id, type='M')
        serializer = MotivationTextSerializer(motivation_texts, many=True, context=self.context)
        return serializer.data

    def get_information_texts(self, obj):
        information_texts = MotivationText.objects.filter(patient__id=obj.id, type='I')
        serializer = MotivationTextSerializer(information_texts, many=True, context=self.context)
        return serializer.data

    def get_o2_min(self, obj):
        threshold_value = ThresholdValue.objects.filter(
            patient_id=obj.id,
            type='O',
            is_upper_threshold=False
        ).last()
        return threshold_value.value if threshold_value else None

    def get_o2_max(self, obj):
        threshold_value = ThresholdValue.objects.filter(
            patient_id=obj.id,
            type='O',
            is_upper_threshold=True
        ).last()
        return threshold_value.value if threshold_value else None

    def get_pulse_min(self, obj):
        threshold_value = ThresholdValue.objects.filter(
            patient_id=obj.id,
            type='P',
            is_upper_threshold=False
        ).last()
        return threshold_value.value if threshold_value else None

    def get_pulse_max(self, obj):
        threshold_value = ThresholdValue.objects.filter(
            patient_id=obj.id,
            type='P',
            is_upper_threshold=True
        ).last()
        return threshold_value.value if threshold_value else None

    def get_temperature_min(self, obj):
        threshold_value = ThresholdValue.objects.filter(
            patient_id=obj.id,
            type='T',
            is_upper_threshold=False
        ).last()
        return threshold_value.value if threshold_value else None

    def get_temperature_max(self, obj):
        threshold_value = ThresholdValue.objects.filter(
            patient_id=obj.id,
            type='T',
            is_upper_threshold=True
        ).last()
        return threshold_value.value if threshold_value else None

    class Meta(PatientListSerializer.Meta):
        fields = PatientListSerializer.Meta.fields + [
            'address',
            'zip_code',
            'city',
            'next_of_kin',
            'motivation_texts',
            'information_texts',
            'o2_min',
            'o2_max',
            'pulse_min',
            'pulse_max',
            'temperature_min',
            'temperature_max',
            'activity_access',
            'pulse_access',
            'o2_access',
            'temperature_access',
            'show_activity',
            'show_pulse',
            'show_o2',
            'show_temperature'
        ]


class CurrentPatientSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()
    motivation_texts = serializers.SerializerMethodField('get_motivation_texts')
    information_texts = serializers.SerializerMethodField('get_information_texts')

    def get_motivation_texts(self, obj):
        motivation_texts = MotivationText.objects.filter(patient=obj, type='M')
        serializer = MotivationTextSerializer(motivation_texts, many=True, context=self.context)
        return serializer.data

    def get_information_texts(self, obj):
        information_texts = MotivationText.objects.filter(patient=obj, type='I')
        serializer = MotivationTextSerializer(information_texts, many=True, context=self.context)
        return serializer.data

    class Meta:
        model = Patient
        fields = [
            'id',
            'user',
            'motivation_texts',
            'information_texts',
            'activity_access',
            'pulse_access',
            'o2_access',
            'temperature_access'
        ]


class PatientGraphSeriesSerializer(serializers.ModelSerializer):
    measurements = serializers.SerializerMethodField('get_measurements')
    lower_threshold_values = serializers.SerializerMethodField('get_lower_threshold_values')
    upper_threshold_values = serializers.SerializerMethodField('get_upper_threshold_values')

    class Meta:
        model = Patient
        fields = ('measurements', 'lower_threshold_values', 'upper_threshold_values')

    def get_measurements(self, obj):
        measurements = Measurement.objects.filter(
            patient=obj,
            type=self.context['type'],
            time__gte=self.context['min_time']
        )
        if 'exclude_measurement_alarms' in self.context and self.context['exclude_measurement_alarms']:
            serializer = MeasurementGraphSeriesSerializer(measurements, many=True)
            return serializer.data
        else:
            measurement_ids = map(lambda measurement: measurement.id, measurements)
            alarms = Alarm.objects.filter(measurement_id__in=measurement_ids)
            alarm_dict = dict((alarm.measurement_id, alarm) for alarm in alarms)  # key is measurement id
            serializer = MeasurementGraphSeriesSerializer(measurements, many=True, alarm_dict=alarm_dict)
            return serializer.data

    def get_lower_threshold_values(self, obj):
        queryset = ThresholdValue.objects.filter(patient=obj, type=self.context['type'], is_upper_threshold=False)
        serializer = ThresholdValueGraphSeriesSerializer(queryset, many=True)
        return serializer.data

    def get_upper_threshold_values(self, obj):
        queryset = ThresholdValue.objects.filter(patient=obj, type=self.context['type'], is_upper_threshold=True)
        serializer = ThresholdValueGraphSeriesSerializer(queryset, many=True)
        return serializer.data
