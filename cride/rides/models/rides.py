"""Rides model."""

# Django
from django.db import models

# Utilities
from cride.utils.models import CRideModel

class Ride(CRideModel):
    """Ride model"""

    offered_by = models.ForeignKey("users.User",on_delete=models.SET_NULL,null=True)       
    offered_in = models.ForeignKey('circles.Circle',on_delete=models.CASCADE,null=True)

    passengers =  models.ManyToManyField("users.User",related_name='passengers')

    aviable_seats = models.PositiveSmallIntegerField(default=1)
    comments = models.TextField(blank=True)

    departure_location = models.CharField(max_length=255)
    departure_date = models.models.DateTimeField()
    arrival_location = models.CharField(max_length=255)
    arrival_date = models.models.DateTimeField()

    rating = models.FloatField(null=True)

    is_active = models.BooleanField(
        'active status',
        default=True,
        help_text='Used for disabling the ride or marking it as finished.'
    )

    def __str__(self):
        """Return ride details."""
        return f"""
        From {self.departure_location} to {self.arrival_location} | 
        {self.departure_date.strftime(%a %d,%b)} 
        starts: {self.departure_date.strftime(%I:%M %p)} 
        arrives: {self.arrival_date.strftime(%I:%M %p)}
        """


