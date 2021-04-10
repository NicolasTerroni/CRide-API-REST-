"""Membership views"""

# Django REST Framework
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

# Models
from cride.circles.models import Circle, Membership

# Serializers
from cride.circles.serializers import MembershipModelSerializer

# Permissions
from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions.memberships import IsActiveCircleMember

class MembershipViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet,):
    """Circle membership viewset."""

    serializer_class = MembershipModelSerializer
    
    def dispatch(self,request,*args,**kwargs):
        """Verify that the circle exists."""
        slug_name = kwargs['slug_name']
        self.circle = get_object_or_404(Circle,slug_name=slug_name)
        return super(MembershipViewSet, self).dispatch(request,*args,**kwargs)

    def get_permissions(self):
        """Assign permissions based on actions."""
        permissions = [IsAuthenticated, IsActiveCircleMember]
        return [permission() for permission in permissions]
    
    def get_queryset(self):
        """Return circle members."""
        return Membership.objects.filter(
            circle=self.circle,
            is_active=True,
        )

    def get_object(self):
        """Return the circle member by its username."""
        return get_object_or_404(
            Membership,
            user__username=self.kwargs['pk'],
            circle=self.circle,
            is_active=True,
        )
    
    def perform_destroy(self,instance):
        """Disable membership"""
        instance.is_active = False
        instance.save()


    @action(detail=True,methods=['get'])
    def invitations(self,request,*args,**kwargs):
        """Retrieve a member's invitation breakdown.
        
        Will return a list containin all the members that
        have used its invitations and another list containing
        the invitations taht haven't been used yet.
        """
        invited_members = Membership.objects.filter(
            circle=self.circle,
            invited_by=request.user,
            is_active=True,
        )
        data = {
            'used_invitations': MembershipModelSerializer(invited_members,many=True).data
        }
        return Response(data)