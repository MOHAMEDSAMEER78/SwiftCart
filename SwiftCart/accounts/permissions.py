# accounts/permissions.py
from rest_framework.permissions import BasePermission

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Customer').exists()

class IsSalesManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Sales Manager').exists()

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Admin').exists()
