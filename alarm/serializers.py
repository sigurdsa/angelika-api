from .models import Alarm
from rest_framework import serializers
from measurement.serializers import AlarmMeasurementSerializer


class AlarmSerializer(serializers.ModelSerializer):
    measurement = AlarmMeasurementSerializer()

    class Meta:
        model = Alarm
        fields = ('measurement', 'time_created', 'is_treated')
