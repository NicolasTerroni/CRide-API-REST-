"""Ride views"""

# Django REST Framework
from rest_framework import mixins, viewsets

# Permissions
from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions.memberships import IsActiveCircleMember

# Serializers
from cride.rides.serializers import CreateRideSerialiazer

# Model
from cride.circles.models import Circle

# Mixins
from cride.circles.mixins.circles import AddCircleMixin


class RideViewSet(  AddCircleMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    """Rides view set."""

    serializer_class = CreateRideSerialiazer
    permssion_classes = [IsAuthenticated, IsActiveCircleMember]

    def get_serializer_context(self):
        """Add circle to serializer context."""
        context = super(RideViewSet, self).get_serializer_context()
        context['circle'] = self.circle
        return context
