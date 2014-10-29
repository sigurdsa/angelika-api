from rest_framework import serializers
from measurement.models import Measurement
from calendar import timegm


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
