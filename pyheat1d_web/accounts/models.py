from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from pyheat1d_web.accounts.managers import UserManager


class CreationModificationBase(models.Model):
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    modified_at = models.DateTimeField("Modificado em", auto_now=True)

    class Meta:
        abstract = True


class CustomUser(PermissionsMixin, CreationModificationBase, AbstractBaseUser):
    name = models.CharField("Nome completo", max_length=120)
    email = models.EmailField("Email", unique=True)

    is_staff = models.BooleanField("staff status", default=False)
    is_active = models.BooleanField("Ativo", default=True)

    class Meta:
        verbose_name = "usuário"
        verbose_name_plural = "usuários"
        abstract = False

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def clean(self):
        self.email = self.__class__.objects.normalize_email(self.email)
