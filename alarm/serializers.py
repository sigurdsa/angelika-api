from .models import Alarm
from rest_framework import serializers


class AlarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alarm
        fields = ('time_created', 'is_treated', 'treated_text')