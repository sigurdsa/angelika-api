from .models import MotivationText
from rest_framework import viewsets
from .serializers import MotivationTextSerializer

class MotivationTextViewSet(viewsets.ModelViewSet):
    """
    API endpoint that shows all alarms
    """
    queryset = MotivationText.objects.all()
    serializer_class = MotivationTextSerializer
