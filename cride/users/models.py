"""User model"""

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser

# Utilities
from cride.utils.models import CRideModel

class User(CRideModel, AbstractUser):
    """Custom user model.
    
    Extends from Django's AbstractUser and our CRideModel.
    Changes username field to email and adds some extra fields.
    """
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique':'A user with that email already exists.'
        },
        max_length=254)
    
    phone_number = models.CharField(max_length=17, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username','first_name', 'last_name')

    is_client = models.BooleanField(
        'client status',
        default=True,
        help_text=(
            'Help easily distinguish users and perform queries.'
            'Clients are the main type of user.'
            ),
        )

    is_verified = models.BooleanField(
        'verified',
        default=False,
        help_text=(
            'Set to True when the user have verified its email address.'
        ),
    )

