"""Membership custom permissions."""
# Models
from cride.circles.models import Membership
# Django REST Framework
from rest_framework.permissions import BasePermission

class IsActiveCircleMember(BasePermission):
    """Allow access only to circles members.
    
    Expects that views implementing this permission have
    a 'circle' atribute assigned."""

    def has_permission(self,request,view):
        """Verify user is an active memeber of the circle."""
        circle = view.circle

        try:
            Membership.objects.get(
                user=request.user,
                circle=view.circle,
                is_active=True
            )
        except Membership.DoesNotExist:
            return False
        return True