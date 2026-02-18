from django.db import models, transaction
from django.utils import timezone
from usuarios.models import Socio
from catalogo.models import Titulo, Ejemplar


class Reserva(models.Model):

    ESTADOS = (
        ('ACTIVA', 'Activa'),
        ('ATENDIDA', 'Atendida'),
        ('CANCELADA', 'Cancelada'),
        ('EXPIRADA', 'Expirada'),
    )

    usuario = models.ForeignKey(
        Socio,
        on_delete=models.PROTECT,
        related_name="reservas"
    )

    titulo = models.ForeignKey(
        Titulo,
        on_delete=models.PROTECT,
        related_name="reservas"
    )

    fecha_reserva = models.DateTimeField(default=timezone.now)
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='ACTIVA'
    )

    class Meta:
        ordering = ['fecha_reserva']
        indexes = [
            models.Index(fields=['fecha_reserva']),
        ]

    def __str__(self):
        return f"Reserva {self.usuario} - {self.titulo}"
