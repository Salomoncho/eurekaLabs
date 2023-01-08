from django.conf import settings
from rest_framework.permissions import BasePermission


class ValidateAPIKeyAccess(BasePermission):
    """Permission Class to validate access to the service"""
    def has_permission(self, request, view):
        """API_KEY value should be in the request header (HTTP_X_API_KEY) to allow access"""
        return request.META.get('HTTP_X_API_KEY') == settings.STOCK_SERVICE_API_KEY
