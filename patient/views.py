from .models import Patient
from rest_framework import viewsets
from .serializers import PatientListSerializer
from .serializers import PatientDetailSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return PatientListSerializer
        else:
            return PatientDetailSerializer
