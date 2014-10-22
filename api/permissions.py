from rest_framework import permissions


class IsHealthProfessional(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='health-professionals').exists()


class IsPatient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='patients').exists()
