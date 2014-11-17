from .models import MotivationText
from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField


class MotivationTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotivationText
        fields = ['id', 'time_created', 'text']
        read_only_fields = ('time_created',)


class MotivationTextWithSoundSerializer(MotivationTextSerializer):
    sound = SerializerMethodField('get_sound')

    class Meta(MotivationTextSerializer.Meta):
        fields = MotivationTextSerializer.Meta.fields + ['sound']

    def get_sound(self, obj):
        if obj.sound:
            return {'url': self.context['request'].build_absolute_uri(obj.sound.url)}
        return {}
