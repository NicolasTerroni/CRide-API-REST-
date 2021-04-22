"""Ride views"""

# Django REST Framework
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions.memberships import IsActiveCircleMember
from cride.rides.permissions.rides import IsRideOwner

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter

# Serializers
from cride.rides.serializers import (
    CreateRideSerialiazer, 
    RideModelSerializer, 
    JoinRideSerializer,
    )

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
        if self.action == 'update':
            return JoinRideSerializer
        return RideModelSerializer

    def get_queryset(self):
        """Return active circles's rides."""
        offset = timezone.now() + timedelta(minutes=20)
        return self.circle.ride_set.filter(
            departure_date__gte=offset,
            is_active=True,
            available_seats__gte=1
        )

    @action(detail=True,methods=['post'])
    def join(self,request,*args,**kwargs):
        """Add requesting user to ride."""
        ride = self.get_object()
        serializer = JoinRideSerializer(
            ride,
            data={'passenger':request.user.pk},
            context={'ride':ride,'circle':self.circle},
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        ride = serializer.save()
        data = RideModelSerializer(ride).data
        return Response(data, status=status.HTTP_200_OK)
