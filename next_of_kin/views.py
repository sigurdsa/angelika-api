from .models import NextOfKin
from rest_framework import viewsets
from .serializers import NextOfKinSerializer


class NextOfKinViewSet(viewsets.ModelViewSet):
    """
    API endpoint that shows all NextOfKin
    """
    queryset = NextOfKin.objects.all()
    serializer_class = NextOfKinSerializer
