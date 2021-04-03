"""Users urls"""

from django.urls import path
from cride.users.views import UserLoginAPIView,UserSignUpAPIView,UserAccountVerificationAPIView

urlpatterns = [
    path('users/login/', UserLoginAPIView.as_view(),name='login'),
    path('users/signup/', UserSignUpAPIView.as_view(),name='signup'),
    path('users/verify/', UserAccountVerificationAPIView.as_view(),name='verify'),
]
