from .models import Alarm
from rest_framework import serializers
from measurement.serializers import AlarmMeasurementSerializer, PatientAlarmMeasurementSerializer


class AlarmSerializer(serializers.ModelSerializer):
    measurement = AlarmMeasurementSerializer()

    class Meta:
        model = Alarm
        fields = ('measurement', 'time_created', 'is_treated')


class PatientAlarmSerializer(serializers.ModelSerializer):
    measurement = PatientAlarmMeasurementSerializer()

    class Meta:
        model = Alarm
        fields = ('measurement', 'time_created', 'is_treated', 'treated_text')
