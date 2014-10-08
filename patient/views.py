from django.shortcuts import render
from .models import Patient
from rest_framework import viewsets
from .serializers import PatientSerializer


class PatientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that shows all alarms
    """
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
