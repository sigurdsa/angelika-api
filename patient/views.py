from .models import Patient
from rest_framework import viewsets
from .serializers import PatientListSerializer
from .serializers import PatientDetailSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404





class PatientViewSet(viewsets.ModelViewSet):
    model=Patient
    def list(self, request):
        queryset = Patient.objects.all()
        serializer_class = PatientListSerializer(queryset,many=True)
        return Response(serializer_class.data)

    def retrieve(self, request, pk=None):
        queryset = Patient.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = PatientDetailSerializer(user)
        return Response(serializer.data)

