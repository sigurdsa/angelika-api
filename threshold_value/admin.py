from django.contrib import admin
from .models import ThresholdValue


class ThresholdValueAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return super(ThresholdValueAdmin, self).get_queryset(request).select_related('patient__user')

admin.site.register(ThresholdValue, ThresholdValueAdmin)
