from rest_framework import permissions
from django.conf import settings


class IsHealthProfessional(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='health-professionals').exists()


class IsPatient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='patients').exists()


class IsHub(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='hubs').exists()


class IsCronClient(permissions.BasePermission):
    def has_permission(self, request, view):
        cron_key = request.QUERY_PARAMS.get('cron_key', None)
        return cron_key == settings.CRON_KEY
