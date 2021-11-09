from rest_framework import serializers

from .models import Candidate, User, Vote


class VoteSerializer(serializers.ModelSerializer):
    number = serializers.IntegerField(source="candidate.number", read_only=True)
    name = serializers.CharField(source="candidate.name", read_only=True)
    time = serializers.DateTimeField(source="created_at")
    class Meta:
        model = Vote
        fields = ("id", "number", "name", "time")

class UserSerializer(serializers.ModelSerializer):
    vote = VoteSerializer()

    class Meta:
        model = User
        fields = ("id", "email", "full_name", "vote")

    def get_vote(self, obj):
        if obj.vote is None:
            return None
        return {"number": obj.vote.candidate.number, "name": obj.vote.candidate.name, "time": obj.vote.created_at}


class CandidateListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Candidate
        fields = ("number", "photo", "name")

class CandidateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Candidate
        fields = ("number", "photo", "name", "bio")



