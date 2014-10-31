from rest_framework import serializers
from measurement.models import Measurement
from threshold_value.models import ThresholdValue
from calendar import timegm


class GraphSeriesSerializer(serializers.ModelSerializer):
    x = serializers.SerializerMethodField('get_time')
    y = serializers.SerializerMethodField('get_value')

    class Meta:
        fields = ('x', 'y')

    def get_time(self, obj):
        return int(timegm(obj.time.utctimetuple())) * 1000  # Milliseconds since epoch, UTC

    def get_value(self, obj):
        return obj.value


class MeasurementGraphSeriesSerializer(GraphSeriesSerializer):
    class Meta(GraphSeriesSerializer.Meta):
        model = Measurement


class ThresholdValueGraphSeriesSerializer(GraphSeriesSerializer):
    class Meta(GraphSeriesSerializer.Meta):
        model = ThresholdValue
