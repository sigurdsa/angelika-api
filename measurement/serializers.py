from .models import Measurement
from rest_framework import serializers


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ('time_created', 'value')
