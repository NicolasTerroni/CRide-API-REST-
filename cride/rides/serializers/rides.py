"""Rides Serializer"""

# Django REST Framework
from rest_framework import serializers

# Models
from cride.rides.models.rides import Ride

# Utilities
from datetime import timedelta
from django.utils import timezone

class CreateRideSerialiazer(serializers.ModelSerializer):
    """Create ride serializer."""

    offered_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    available_seats = serializers.IntegerField(min_value=1,max_value=15)


    class Meta:
        """Meta class."""
        model = Ride
        exclude = ('offered_in','passengers','rating','is_active')

    def validate_departure_date(self,data):
        """Verify date is not in the past."""
        min_date = timezone.now() + timedelta(minutes=20)
        if data < min_date:
            raise serializers.ValidationError(
                "Departure time must be at least in 20 minutes."
            )
        return data

