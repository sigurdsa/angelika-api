from django.contrib.auth.models import User
from .models import Patient
from rest_framework import serializers
import datetime
from next_of_kin.models import NextOfKin
from next_of_kin.serializers import NextOfKinSerializer

class SimpleUserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField('get_full_name')

    class Meta:
        model = User
        fields = ['full_name',]

    def get_full_name(self, obj):
        return obj.get_full_name()


class SimplePatientSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()

    class Meta:
        model = Patient
        fields = ('id', 'user')


class PatientListSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()
    birth_date = serializers.SerializerMethodField('get_birth_date')
    age = serializers.SerializerMethodField('get_age')

    def get_birth_date(self, obj):
        return obj.national_identification_number[0:2] + "." \
            + obj.national_identification_number[2:4] + "." \
            + obj.national_identification_number[4:6]

    def get_age(self, obj):
        today = datetime.datetime.today()
        ddmm = obj.national_identification_number[0:4]
        yyyy = "20" + obj.national_identification_number[4:6]
        if int(yyyy) >= today.year:
            yyyy = str(int(yyyy) - 100)
        birth_date = datetime.datetime.strptime(ddmm + yyyy, "%d%m%Y")
        diff = today - birth_date
        num_years = int(diff.days / 365.2425)  # rough estimate, can be wrong in some edge cases
        return num_years

    class Meta:
        model = Patient
        fields = (
            'id',
            'user',
            'birth_date',
            'age',
            'national_identification_number',
            'phone_number'
        )


class PatientDetailSerializer(PatientListSerializer):
    user = SimpleUserSerializer()
    birth_date = serializers.SerializerMethodField('get_birth_date')
    age = serializers.SerializerMethodField('get_age')
    next_of_kin = serializers.SerializerMethodField('get_next_of_kin')

    def get_next_of_kin(self, obj):
        next_of_kin = NextOfKin.objects.filter(patient__id=obj.id)
        serializer = NextOfKinSerializer(next_of_kin, many=True, context=self.context)
        return serializer.data

    class Meta:
        model = Patient
        fields = (
            'id',
            'user',
            'birth_date',
            'age',
            'national_identification_number',
            'phone_number',
            'address',
            'next_of_kin',
            'pulse_max',
            'pulse_min',
            'o2_max',
            'o2_min',
            'temperature_max',
            'temperature_min',
            'activity_access',
            'pulse_access',
            'o2_access',
            'temperature_access'
        )
