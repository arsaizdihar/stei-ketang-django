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
    path("vote/", VoteView.as_view(), name="vote")
] + router.urls
