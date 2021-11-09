
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, views, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from api.models import Candidate, Vote
from api.serializers import (CandidateListSerializer, CandidateSerializer,
                             UserSerializer, VoteSerializer)


class MeView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class CandidateViewSet(viewsets.ReadOnlyModelViewSet):
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

