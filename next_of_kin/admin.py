from django.contrib import admin
from .models import NextOfKin


class NextOfKinAdmin(admin.ModelAdmin):
    model = NextOfKin

    def get_queryset(self, request):
        return super(NextOfKinAdmin, self).get_queryset(request).select_related('patient__user')

admin.site.register(NextOfKin, NextOfKinAdmin)
