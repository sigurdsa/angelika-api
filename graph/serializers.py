from rest_framework import serializers
from measurement.models import Measurement
from threshold_value.models import ThresholdValue
from calendar import timegm
from alarm.models import Alarm


class GraphSeriesSerializer(serializers.ModelSerializer):
    x = serializers.SerializerMethodField('get_time')
    y = serializers.SerializerMethodField('get_value')

    class Meta:
        fields = ['x', 'y']

    def get_time(self, obj):
        return int(timegm(obj.time.utctimetuple())) * 1000  # Milliseconds since epoch, UTC

    def get_value(self, obj):
        return obj.value


class MeasurementGraphSeriesSerializer(GraphSeriesSerializer):
    alarm = serializers.SerializerMethodField('get_alarm')

    def __init__(self, *args, **kwargs):
        self.alarm_dict = kwargs.pop('alarm_dict', None)
        super(MeasurementGraphSeriesSerializer, self).__init__(*args, **kwargs)
        if not self.alarm_dict:
            self.fields.pop('alarm')

    def get_alarm(self, obj):
        if obj.id in self.alarm_dict:
            alarm = self.alarm_dict[obj.id]
            serializer = SimpleAlarmSerializer(alarm)
            return serializer.data
        return None

    class Meta(GraphSeriesSerializer.Meta):
        model = Measurement
        fields = GraphSeriesSerializer.Meta.fields + ['alarm']


class ThresholdValueGraphSeriesSerializer(GraphSeriesSerializer):
    class Meta(GraphSeriesSerializer.Meta):
        model = ThresholdValue

class SimpleAlarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alarm
        fields = ('id', 'time_created', 'is_treated', 'treated_text')
