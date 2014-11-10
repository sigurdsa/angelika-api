from django.contrib import admin
from .models import Alarm
from django import forms
from measurement.models import Measurement


class CustomAlarmForm(forms.ModelForm):
    class Meta:
        model = Alarm
        exclude = []

    def __init__(self, *args, **kwargs):
        super(CustomAlarmForm, self).__init__(*args, **kwargs)
        self.fields['measurement'].queryset = Measurement.objects.filter(alarm__isnull=True, type__in=['O', 'P', 'T'])


class AlarmAdmin(admin.ModelAdmin):
    form = CustomAlarmForm
    model = Alarm

    def get_queryset(self, request):
        return super(AlarmAdmin, self).get_queryset(request).select_related('measurement__patient__user')

admin.site.register(Alarm, AlarmAdmin)
