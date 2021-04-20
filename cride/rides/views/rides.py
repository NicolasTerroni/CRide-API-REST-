"""Ride views"""

# Django REST Framework
from rest_framework import mixins, viewsets

# Permissions
from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions.memberships import IsActiveCircleMember
from cride.rides.permissions.rides import IsRideOwner

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter

# Serializers
from cride.rides.serializers import CreateRideSerialiazer, RideModelSerializer

# Model
from cride.circles.models import Circle

# Mixins
from cride.circles.mixins.circles import AddCircleMixin

# Utilities
from datetime import timedelta
from django.utils import timezone


class RideViewSet(  AddCircleMixin,
                    mixins.ListModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    """Rides view set."""

    # Filters
    filter_backends = (SearchFilter, OrderingFilter)
    ordering = ('departure_date','arrival_date', 'available_seats')
    ordering_fields = ('departure_date', 'arrival_date', 'available_seats')
    search_fields = ('departure_location','arrival_location')


    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated, IsActiveCircleMember]
        if self.action in ['update','partial_update']:
            permissions.append(IsRideOwner)
        return [permission() for permission in permissions]

    def get_serializer_context(self):
        """Add circle to serializer context."""
        context = super(RideViewSet, self).get_serializer_context()
        context['circle'] = self.circle
        return context

    def get_serializer_class(self):
        """Return serializer based on action."""
        if self.action == 'create':
            return CreateRideSerialiazer
        return RideModelSerializer

    def get_queryset(self):
        """Return active circles's rides."""
        offset = timezone.now() + timedelta(minutes=20)
        return self.circle.ride_set.filter(
            departure_date__gte=offset,
            is_active=True,
            available_seats__gte=1
        )