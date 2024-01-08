from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField("Data de criação", auto_now_add=True)
    modified_at = models.DateTimeField("Data de modificação", auto_now=True)

    class Meta:
        abstract = True


class Simulation(BaseModel):
    class Status(models.TextChoices):
        INIT = "I", "Simulação pronta para execução"
        RUNNING = "R", "Rodando"
        SUCCESS = "S", "Simulação executada"
        FAILED = "F", "Simulação Falhou"

    # input_file = models.FilePathField(path=settings.MEDIA_ROOT)  # TODO: Trocar por FileField
    input_file = models.CharField(max_length=10)
    status = models.CharField("Status", max_length=1, choices=Status.choices, default=Status.INIT)

    tag = models.SlugField("Tag", unique=True)

    length = models.FloatField("Comprimento", default=1.0)
    ndiv = models.IntegerField("Numero de divisões", default=1_000)

    dt = models.FloatField("Passo de Tempo", default=1.0e-01)
    nstep = models.IntegerField("Número de Passos", default=1_000)

    initialt = models.FloatField("Temperatura Inicial", default=0.0)
    lbc_value = models.FloatField("Temperatura a esquerda", default=10.0)
    rbc_value = models.FloatField("Temperatura a direita", default=-10.0)

    def __str__(self):
        return self.tag
