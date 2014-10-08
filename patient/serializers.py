from .models import Patient
from rest_framework import serializers


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ('national_identification_number',
    'telephone',
    'address',
    'pulse_max',
    'pulse_min',
    'o2_max',
    'o2_min',
    'temperature_max',
    'temperature_min',
    'activity_max',
    'activity_min',
    'activity_access',
    'pulse_access',
    'o2_access',
    'temperature_access')
