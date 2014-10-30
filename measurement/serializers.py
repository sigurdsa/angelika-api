from .models import Measurement
from rest_framework import serializers
from calendar import timegm
from patient.serializers import SimplePatientSerializer


class MeasurementGraphSerializer(serializers.ModelSerializer):
    x = serializers.SerializerMethodField('get_time')
    y = serializers.SerializerMethodField('get_value')

    class Meta:
        model = Measurement
        fields = ('x', 'y')

    def get_time(self, obj):
        return int(timegm(obj.time.utctimetuple())) * 1000  # Milliseconds since epoch, UTC

    def get_value(self, obj):
        return obj.value


class AlarmMeasurementSerializer(serializers.ModelSerializer):
    patient = SimplePatientSerializer()

    class Meta:
        model = Measurement
        fields = ('patient', 'type')


class PatientAlarmMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ('type', 'value')
