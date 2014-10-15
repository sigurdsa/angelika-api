from .models import NextOfKin
from rest_framework import serializers


class NextOfKinSerializer(serializers.ModelSerializer):
    class Meta:
        model = NextOfKin
