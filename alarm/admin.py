from django.contrib import admin
from .models import Alarm


class AlarmAdmin(admin.ModelAdmin):
    model = Alarm

    def get_queryset(self, request):
        return super(AlarmAdmin, self).get_queryset(request).select_related('measurement__patient__user')

admin.site.register(Alarm, AlarmAdmin)
