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

            group = None
            if user.groups.filter(name='health-professionals').exists():
                group = 'health-professionals'
            elif user.groups.filter(name='patients').exists():
                group = 'patients'
            elif user.groups.filter(name='hubs').exists():
                group = 'hubs'

            token, created = Token.objects.get_or_create(user=user)

            return Response({'token': token.key, 'group': group})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

custom_obtain_auth_token = CustomObtainAuthToken.as_view()
