from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Patient
from django import forms

class CustomPatientForm(forms.ModelForm):
    class Meta:
        model = Patient

    def __init__(self, *args, **kwargs):
        super(CustomPatientForm, self).__init__(*args, **kwargs)
        self.fields['hub'].queryset = Group.objects.get(name="hubs").user_set.all()
        self.fields['user'].queryset = Group.objects.get(name="patients").user_set.all()


class PatientAdmin(admin.ModelAdmin):
    form = CustomPatientForm

admin.site.register(Patient, PatientAdmin)
