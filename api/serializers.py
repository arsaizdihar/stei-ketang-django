from django.core.signing import BadSignature, Signer
from rest_framework import serializers
from users.models import ChangePasswordKey

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


class SetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, style={'input_type': 'password'}, trim_whitespace=False)
    password2 = serializers.CharField(min_length=8, style={'input_type': 'password'}, trim_whitespace=False)
    code = serializers.CharField()


    def validate(self, attrs):
        errs = {}
        if attrs["password"] != attrs["password2"]:
            errs["password"] = "Two passwords must be same."
        code = attrs["code"]
        signer = Signer()
        try:
            data = signer.unsign(code)
            key: ChangePasswordKey = ChangePasswordKey.objects.get(id=data)
            if key.used:
                errs["code"] = "Password already set."
            elif not errs:
                user = key.user
                user.set_password(attrs["password"])
                key.used = True
                key.save()
        except (BadSignature, ChangePasswordKey.DoesNotExist):
            errs["code"] = "Code invalid."
        if errs:
            raise serializers.ValidationError(errs)
        return super().validate(attrs)



