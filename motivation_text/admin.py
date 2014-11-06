from django.contrib import admin
from .models import MotivationText


class MotivationTextAdmin(admin.ModelAdmin):
    model = MotivationText

    def get_queryset(self, request):
        return super(MotivationTextAdmin, self).get_queryset(request).select_related('patient__user')

admin.site.register(MotivationText, MotivationTextAdmin)
