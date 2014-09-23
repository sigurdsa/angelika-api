from .models import Alarm
from rest_framework import viewsets
from .serializers import AlarmSerializer


class AlarmViewSet(viewsets.ModelViewSet):
    """
    API endpoint that shows all alarms
    """
    queryset = Alarm.objects.all()
    serializer_class = AlarmSerializer
