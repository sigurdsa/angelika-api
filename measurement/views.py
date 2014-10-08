from .models import Measurement
from rest_framework import viewsets
from .serializers import MeasurementSerializer
from django.contrib.auth.models import User


class AlarmViewSet(viewsets.ModelViewSet):
    """
    API endpoint that shows measurment from one patient
    """
    serializer_class = MeasurementSerializer

    def get_queryset(self):
        queryset = Measurement.objects.none()
        username = self.request.QUERY_PARAMS.get('user_id', None)
        if username is not None:
            queryset = queryset.filter(purchaser__username=username)
        return queryset
