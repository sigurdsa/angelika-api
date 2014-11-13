from .models import Alarm
from rest_framework import serializers
from measurement.serializers import AlarmMeasurementSerializer, PatientAlarmMeasurementSerializer


class AlarmSerializer(serializers.ModelSerializer):
    measurement = AlarmMeasurementSerializer()

    class Meta:
        model = Alarm
        fields = (
            'id',
            'measurement',
            'time_created',
            'is_treated',
            'reason'
        )


class PatientAlarmSerializer(serializers.ModelSerializer):
    measurement = PatientAlarmMeasurementSerializer()

    class Meta:
        model = Alarm
        fields = (
            'id',
            'measurement',
            'time_created',
            'is_treated',
            'treated_text',
            'search_tag',
            'reason'
        )
