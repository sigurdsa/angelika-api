from .models import Measurement
from rest_framework import viewsets
from .serializers import MeasurementSerializer
from django.contrib.auth.models import User


class MeasurementViewSet(viewsets.ModelViewSet):
    """
    API endpoint that shows measurement from one patient
    """
    serializer_class = MeasurementSerializer

    def get_queryset(self):
        queryset = Measurement.objects.none()
        user_id = self.request.QUERY_PARAMS.get('user_id', None)
        if user_id is not None:
            queryset = queryset.filter(user__id=user_id)
        return queryset
