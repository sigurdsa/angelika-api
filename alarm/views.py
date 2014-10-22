from .models import Alarm
from rest_framework import viewsets
from .serializers import AlarmSerializer
from api.permissions import IsHealthProfessional
from rest_framework.permissions import IsAuthenticated


class AlarmViewSet(viewsets.ModelViewSet):
    """
    API endpoint that shows all alarms
    """
    permission_classes = (IsAuthenticated, IsHealthProfessional,)
    queryset = Alarm.objects.all()
    serializer_class = AlarmSerializer
