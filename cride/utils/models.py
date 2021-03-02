"""Django models utilities"""

# Django
from django.db import models

class CRideModel(models.Model):
    """Comparte Ride base model.

    An abstract base class that every model in
    the project will inherit. This class provides every table
    with the following atributes:
        + created (DateTime): Stores the datetime the object was created.
        + modified (DateTime): Stores the last datetime the object was modified.
    """

    created = models.DateTimeField(
        'created_at',
        auto_now_add = True,
        help_text='Date time on which the object was created.',
    )

    modified = models.DateTimeField(
        'modified_at',
        auto_now = True,
        help_text='Last date time on which the object was modified.',
    )

    class Meta:
        abstract = True
        get_latest_by =  'created'
        ordering = ('-created','-modified')