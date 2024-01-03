from django.conf import settings
from django.db import models


class Simulation(models.Model):
    class Status(models.TextChoices):
        INIT = "I", "Simulação pronta para execução"
        RUNNING = "R", "Rodando"
        SUCCESS = "S", "Simulação executada"
        FAILED = "F", "Simulação Falhou"

    tag = models.SlugField("Tag", unique=True)
    input_file = models.FilePathField(path=settings.MEDIA_ROOT)
    status = models.CharField("Status", max_length=1, choices=Status.choices, default=Status.INIT)

    def __str__(self):
        return f"<Tag={self.tag}, Status={self.get_status_display()}>"
