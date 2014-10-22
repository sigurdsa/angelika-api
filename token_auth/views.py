from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from patient.models import Patient


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request):
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            user = serializer.object['user']
            patient = None
            try:
                patient = Patient.objects.get(user__id=user.id)
            except Patient.DoesNotExist:
                pass

            token, created = Token.objects.get_or_create(user=user)

            role = 'patient' if patient else 'health-professional'
            return Response({'token': token.key, 'role': role})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

custom_obtain_auth_token = CustomObtainAuthToken.as_view()
