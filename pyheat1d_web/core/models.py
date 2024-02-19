from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models


# TODO: Reti
class BaseModel(models.Model):
    created_at = models.DateTimeField("Data de criação", auto_now_add=True)
    modified_at = models.DateTimeField("Data de modificação", auto_now=True)

    class Meta:
        abstract = True


def greater_than_zero(value):
    if value <= 0:
        raise ValidationError("Número tem que ser maior que zero.")


class Simulation(BaseModel):
    class Status(models.TextChoices):
        INIT = "I", "Simulação pronta para execução"
        RUNNING = "R", "Rodando"
        SUCCESS = "S", "Simulação executada"
        FAILED = "F", "Simulação Falhou"

    # input_file = models.FilePathField(path=settings.MEDIA_ROOT)  # TODO: Trocar por FileField
    input_file = models.CharField(max_length=1024)
    status = models.CharField("Status", max_length=1, choices=Status.choices, default=Status.INIT)

    tag = models.SlugField("Tag")

    length = models.FloatField("Comprimento", default=1.0, validators=[greater_than_zero])
    ndiv = models.IntegerField("Numero de divisões", default=1_000, validators=[greater_than_zero])

    dt = models.FloatField("Passo de Tempo", default=1.0e-01, validators=[greater_than_zero])
    nstep = models.IntegerField("Número de Passos", default=1_000, validators=[greater_than_zero])

    initialt = models.FloatField("Temperatura Inicial", default=0.0)
    lbc_value = models.FloatField("Temperatura a esquerda", default=10.0)
    rbc_value = models.FloatField("Temperatura a direita", default=-10.0)

    celery_task = models.UUIDField(null=True, blank=True)

    user = models.ForeignKey(get_user_model(), verbose_name="user", on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["tag", "user"], name="unique_tag_user")]

    def __str__(self):
        return self.tag
