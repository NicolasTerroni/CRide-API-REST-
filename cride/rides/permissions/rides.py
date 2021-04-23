"""Rides permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission

class IsRideOwner(BasePermission):
    """Verify requesting user is the ride publisher."""

    def has_object_permission(self,request,view,obj):
        """Verify requesting user is the ride publisher."""
        return request.user == obj.offered_by

class IsNotRideOwner(BasePermission):
    """Verify requesting user is not the ride publisher."""

    message = "The ride owner can't be a passenger."

    def has_object_permission(self,request,view,obj):
        """Verify requesting user is not the ride publisher."""
        return not request.user == obj.offered_by