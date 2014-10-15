from .models import MotivationText
from rest_framework import serializers


class MotivationTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotivationText
        fields = ('time_created', 'text')
