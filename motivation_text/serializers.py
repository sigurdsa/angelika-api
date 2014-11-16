from .models import MotivationText
from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField


class MotivationTextSerializer(serializers.ModelSerializer):
    sound = SerializerMethodField('get_sound')

    class Meta:
        model = MotivationText
        fields = ('id', 'time_created', 'text', 'sound')
        read_only_fields = ('time_created',)

    def get_sound(self, obj):
        if obj.sound:
            return {'url': self.context['request'].build_absolute_uri(obj.sound.url)}
        return None
