"""Invitations tests."""

# Django REST Framework
from rest_framework import status
from rest_framework.test import APITestCase

# Django
from django.test import TestCase

# Models
from cride.circles.models import Invitation, Circle, Membership
from cride.users.models import User
from rest_framework.authtoken.models import Token


class InvitationsManagerTestCase(TestCase):
    """Invitation manager test case."""

    def setUp(self):
        """Test case setup."""
        self.user = User.objects.create(
            first_name="Nicolas",
            last_name="Terroni",
            email="nicooterroni@gmail.com",
            username="NT01",
            password="admin123"
        )
        self.circle = Circle.objects.create(
            name="Facultad UNNOBA",
            slug_name="unnoba",
            about="Unnoba rides",
            verified=True
        )

    def test_code_generation(self):
        """Random codes should be generated automatically."""
        invitation = Invitation.objects.create(
            issued_by=self.user,
            circle=self.circle
        )
        self.assertIsNotNone(invitation.code)

    def test_code_usage(self):
        """If a code is given, there's no need to create a new one."""
        code = "hola"
        invitation = Invitation.objects.create(
            issued_by=self.user,
            circle=self.circle,
            code=code
        )
        self.assertEqual(invitation.code, code)

    def test_code_generation_if_duplicated(self):
        """If given code is not unique, a new one must be generated."""
        code = Invitation.objects.crete(
            issued_by=self.user,
            circle=self.circle
        ).code

        # Create another invitation with the past code.
        invitation = Invitation.objects.crete(
            issued_by=self.user,
            circle=self.circle,
            code=code
        )
        self.assertNotEqual(code, invitation.code)


class MemberInvitationAPITestCase(APITestCase):
    """Member invitation API test case."""
    def setUp(self):
        """Test case setup."""
        self.user = User.objects.create(
            first_name="Nicolas",
            last_name="Terroni",
            email="nicooterroni@gmail.com",
            username="NT01",
            password="admin123"
        )
        self.profile = Profile.objects.create(
            user=self.user
        )
        self.circle = Circle.objects.create(
            name="Facultad UNNOBA",
            slug_name="unnoba",
            about="Unnoba rides",
            verified=True
        )
        self.membership = Membership.objects.create(
            user=self.user,
            profile=self.profile,
            circle=self.circle,
            remaining_invitations=10
        )

        # Auth
        self.token = Token.objects.create(user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

        # URL
        self.url = f"/circles/{self.circle.slug_name}/members/{self.user.username}/invitations/"


    def test_response_success(self):
        """Verify request succeed."""
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_invitation_creation(self):
        """Verify invitations are generated if none exists previously."""
        # Invitations in DB must be 0
        self.assertEqual(Invitation.objects.count(), 0)

        # Call member invitations URL
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

        # Verify new invitations where created
        invitations = Invitation.objects.filter(issued_by=self.user)
        self.assertEqual(invitations.count(), self.membership.remaining_invitations)
        for invitation in invitations:
            self.assertIn(invitation.code, request.data['invitations'])


