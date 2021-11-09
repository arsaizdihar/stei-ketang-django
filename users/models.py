from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from users.managers import CustomUserManager


class User(AbstractUser):

    username = None
    first_name = None
    last_name = None
    full_name = models.CharField(max_length=50, verbose_name=_("Full Name"))
    email = models.EmailField(
        _("email address"),
        blank=False,
        unique=True,
        error_messages={"unique": _("A user with that email already exists")},
    )

    REQUIRED_FIELDS = ("full_name",)
    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def get_full_name(self):
        return self.full_name

    def __str__(self):
        return self.get_full_name()

    def clean(self):
        super(User, self).clean()
        errors = {}
        if not self.full_name or len(self.full_name) < 4:
            errors["full_name"] = ["Minimum length 4"]
        if errors:
            raise ValidationError(errors)

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

class ChangePasswordKey(models.Model):
    used = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_query_name="change")
