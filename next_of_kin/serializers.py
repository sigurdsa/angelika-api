from .models import NextOfKin
from rest_framework import serializers


class NextOfKinSerializer(serializers.ModelSerializer):
    class Meta:
        model = NextOfKin
        fields = (
            'id',
            'full_name',
            'address',
            'phone_number',
            'priority',
            'relation',
        )
