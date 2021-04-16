"""Circle invitation manager."""

# Django
from django.db import models

# Utilities
import random
from string import ascii_uppercase, digits


class InvitationManager(models.Manager):
    """Invitation manager.
    
    Handle the invitations's codes creation."""

    CODE_LENGTH = 10

    def create(self,**kwargs):
        """Handle code creation."""
        pool = ascii_uppercase + digits + '.-_'
        code = kwargs.get('code', ''.join(random.choices(pool, k=self.CODE_LENGTH)))

        while self.filter(code=code).exists():
            code = ''.join(random.choices(pool, k=self.CODE_LENGTH))
        kwargs['code'] = code

        return super(InvitationManager, self).create(**kwargs)