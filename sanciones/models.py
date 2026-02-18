from django.db import models
from django.utils import timezone
from usuarios.models import Socio


class Sancion(models.Model):

    usuario = models.ForeignKey(
        Socio,
        on_delete=models.PROTECT,
        related_name="sanciones"
    )

    dias_sancion = models.IntegerField()

    fecha_inicio = models.DateTimeField(default=timezone.now)

    fecha_fin = models.DateTimeField()

    activa = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=['fecha_fin']),
            models.Index(fields=['activa']),
        ]

    def __str__(self):
        return f"Sanción {self.usuario} - {self.dias_sancion} días"

    def verificar_estado(self):
        """
        Verifica si la sanción debe desactivarse automáticamente.
        """
        if self.activa and timezone.now() > self.fecha_fin:
            self.activa = False
            self.save()
