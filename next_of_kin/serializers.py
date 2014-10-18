from .models import NextOfKin
from rest_framework import serializers


class NextOfKinSerializer(serializers.ModelSerializer):
    class Meta:
        model = NextOfKin
        fields = (
            'id',
            'first_name',
            'last_name',
            'address',
            'phone_number',
            'relation',
        )

