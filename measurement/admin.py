from django.contrib import admin
from .models import Measurement


class MeasurementAdmin(admin.ModelAdmin):
    model = Measurement

    def get_queryset(self, request):
        return super(MeasurementAdmin, self).get_queryset(request).select_related('patient__user')

admin.site.register(Measurement, MeasurementAdmin)
