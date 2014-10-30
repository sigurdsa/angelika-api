from .models import Measurement
from rest_framework import serializers
from patient.serializers import SimplePatientSerializer


class AlarmMeasurementSerializer(serializers.ModelSerializer):
    patient = SimplePatientSerializer()

    class Meta:
        model = Measurement
        fields = ('patient', 'type')


class PatientAlarmMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ('type', 'value')
