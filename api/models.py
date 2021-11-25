from django.db import models
from users.models import User


class Candidate(models.Model):
    number = models.PositiveSmallIntegerField(unique=True)
    name = models.CharField(max_length=250)
    photo = models.ImageField(upload_to="candidates", null=True)
    active = models.BooleanField(default=True)
    bio = models.TextField()
    instagram = models.CharField(max_length=200, null=True, blank=True)
    linkedin = models.CharField(max_length=200, null=True, blank=True)
    twitter = models.CharField(max_length=200, null=True, blank=True)

    @property
    def visi_query(self):
        return self.details.filter(type=DetailTypes.VISI)

    @property
    def misi_query(self):
        return self.details.filter(type=DetailTypes.MISI)

    @property
    def program_query(self):
        return self.details.filter(type=DetailTypes.PROGRAM)
    

    def __str__(self) -> str:
        return f"{self.number}. {self.name}"

    class Meta:
        ordering = ('number', )


class Vote(models.Model):
    user = models.ForeignKey(User, related_name="votes", on_delete=models.CASCADE)
    session = models.PositiveSmallIntegerField(choices=((1, 1), (2, 2)), default=1)
    candidate = models.ForeignKey(Candidate, related_name="votes", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.email} - {self.candidate.number}"
    
    class Meta:
        unique_together = ['user', 'session']

class DetailTypes(models.IntegerChoices):
        VISI = 1
        MISI = 2
        PROGRAM = 3

class Detail(models.Model):
    candidate = models.ForeignKey(Candidate, related_name="details", on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField()
    text = models.TextField()
    type = models.PositiveSmallIntegerField(choices=DetailTypes.choices, default=DetailTypes.VISI)
    desc = models.TextField(null=True, blank=True)

    @property
    def type_str(self) -> str:
        return DetailTypes(self.type).label

    def __str__(self) -> str:
        return f"{self.candidate.name} - {self.type_str} - {self.number}"

    class Meta:
        ordering = ("number", )

