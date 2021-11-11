
from django.core.signing import BadSignature, Signer
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, views, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from users.models import ChangePasswordKey

from api.models import Candidate, Vote
from api.serializers import (CandidateListSerializer, CandidateSerializer,
                             SetPasswordSerializer, UserSerializer,
                             VoteSerializer)


class MeView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class CandidateViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "number"
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Candidate.objects

    def get_serializer_class(self):
        if self.action == "list":
            return CandidateListSerializer
        return CandidateSerializer


class VoteView(views.APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request: Request, format=None):
        if hasattr(self.request.user, "vote"):
            return Response({"error": "Already voted"}, status=status.HTTP_400_BAD_REQUEST)
        to_vote = get_object_or_404(Candidate, number=request.data.get("number"))
        vote = Vote.objects.create(candidate=to_vote, user=request.user)
        return Response({"status": "success", "vote": VoteSerializer(vote).data})

class SetPasswordView(views.APIView):
    serializer_class = SetPasswordSerializer

    def post(self, request: Request, format=None):
        serializer = SetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"success": True})
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CheckPasswordCodeView(views.APIView):
    def post(self, request: Request, format=None):
        signer = Signer()
        try:
            code = request.data.get("code")
            data = signer.unsign(code)
            key: ChangePasswordKey = ChangePasswordKey.objects.get(id=data)
            if key.used:
                return Response({"error": "Password already set."}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"valid": True})
        except (BadSignature, ChangePasswordKey.DoesNotExist):
            return Response({"error": "Invalid URL."})
