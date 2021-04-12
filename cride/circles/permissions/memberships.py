"""Membership custom permissions."""
# Models
from cride.circles.models import Membership, Invitation
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


class IsSelfMember(BasePermission):
    """Allow access only to member owners."""

    def has_permission(self,request,view):
        """Let objects permission grant access."""
        obj = view.get_object()
        return self.has_object_permission(request,view,obj)

    def has_object_permission(self,request,view,obj):
        """Allow acces only if member is owned by the requesting user."""
        return request.user == obj.user