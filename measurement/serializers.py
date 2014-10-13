from .models import Measurement
from rest_framework import serializers
from calendar import timegm


class MeasurementSerializer(serializers.ModelSerializer):
    time = serializers.SerializerMethodField('get_time')

    class Meta:
        model = Measurement
        fields = ('time', 'value')

    def get_time(self, obj):
        return int(timegm(obj.time.utctimetuple())) * 1000  # Milliseconds since epoch, UTC
