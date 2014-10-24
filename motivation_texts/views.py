from .models import MotivationText
from .serializers import MotivationTextSerializer
from api.permissions import IsHealthProfessional, IsPatient
from rest_framework.permissions import IsAuthenticated
