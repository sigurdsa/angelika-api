from rest_framework.views import APIView
from api.permissions import IsCronClient
from rest_framework.response import Response
from .models import MotivationText
from django.utils import timezone
from datetime import timedelta


class DeleteOldMotivationTexts(APIView):
    """
    Run every night. Deletes motivation texts that are older than one month.
    """
    permission_classes = (IsCronClient,)

    def post(self, request, format=None):
        rows_to_delete = MotivationText.objects.filter(
            type='M',
            time_created__lte=timezone.now() - timedelta(days=31)
        )
        num_deleted_rows = rows_to_delete.count()
        rows_to_delete.delete()

        return Response({'num_deleted_rows': num_deleted_rows})
