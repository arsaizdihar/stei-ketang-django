from django.conf import settings
from django.core.signing import BadSignature, Signer
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from users.models import ChangePasswordKey

from .models import Candidate, Detail, User, Vote


class VoteSerializer(serializers.ModelSerializer):
    number = serializers.IntegerField(source="candidate.number", read_only=True)
    name = serializers.CharField(source="candidate.name", read_only=True)
    photo = serializers.SerializerMethodField()
    time = serializers.DateTimeField(source="created_at")

    def get_photo(self, obj):
        if obj.candidate.photo is None:
            return None
        request = self.context.get('request')
        return request.build_absolute_uri(obj.candidate.photo.url)
    class Meta:
        model = Vote
        fields = ("id", "number", "name", "time", "photo", "session")

class UserSerializer(serializers.ModelSerializer):
    vote = SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "email", "full_name", "vote")

    def get_vote(self, obj):
        vote = obj.votes.filter(session=settings.VOTE_SESSION).first()
        if vote is None:
            return None
        return VoteSerializer(vote, context=self.context).data

class CandidateListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Candidate
        fields = ("number", "photo", "name")

class DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detail
        fields = ("number", "text")

class CandidateSerializer(serializers.ModelSerializer):
    detail = serializers.SerializerMethodField()


    def get_detail(self, obj):
        visi = DetailSerializer(obj.visi_query, many=True)
        misi = DetailSerializer(obj.misi_query, many=True)
        program = DetailSerializer(obj.program_query, many=True)

        return {"visi": visi.data, "misi": misi.data, "program": program.data}
    
    class Meta:
        model = Candidate
        exclude = ("id",)


class SetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, style={'input_type': 'password'}, trim_whitespace=False)
    password2 = serializers.CharField(min_length=8, style={'input_type': 'password'}, trim_whitespace=False)
    code = serializers.CharField(required=True)


    def validate(self, attrs):
        errs = {}
        if attrs["password"] != attrs["password2"]:
            errs["password"] = "Two passwords must be same."
        code = attrs["code"]
        signer = Signer()
        try:
            data = signer.unsign_object(code or "")
            key: ChangePasswordKey = ChangePasswordKey.objects.get(user__email=data.get("email"))
            if key.used:
                errs["code"] = "Password already set."
            elif not errs:
                user = key.user
                user.set_password(attrs["password"])
                user.save()
                key.used = True
                key.save()
        except (BadSignature, ChangePasswordKey.DoesNotExist, TypeError):
            errs["code"] = "Code invalid."
        if errs:
            raise serializers.ValidationError(errs)
        return super().validate(attrs)



