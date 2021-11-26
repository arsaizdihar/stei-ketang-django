from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import *

router = DefaultRouter()
router.register('candidates', CandidateViewSet, basename='candidate')

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="register"),
    path("me/", MeView.as_view(), name="me"),
    path("vote/status/", VotingStatusView.as_view(), name="voting-status"),
    path("vote/", VoteView.as_view(), name="vote"),
    path("password/set/", SetPasswordView.as_view(), name="set-password"),
    path("password/check/", CheckPasswordCodeView.as_view(), name="check-password"),
    path("vote/count/", VoteCountView.as_view(), name="vote-count")
] + router.urls
