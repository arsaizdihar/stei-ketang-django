from django.db import models
from users.models import User


class Candidate(models.Model):
    number = models.PositiveSmallIntegerField(unique=True)
    name = models.CharField(max_length=250)
    photo = models.ImageField(upload_to="candidates", null=True)
    bio = models.TextField()

    def __str__(self) -> str:
        return f"{self.number}. {self.name}"


class Vote(models.Model):
    user = models.OneToOneField(User, unique=True, related_query_name="vote", on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, related_query_name="votes", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.email} - {self.candidate.number}"
    

