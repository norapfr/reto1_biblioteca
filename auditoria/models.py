from django.db import models
from django.utils import timezone
from usuarios.models import UsuarioInterno


class Auditoria(models.Model):

    ACCIONES = (
        ('CREACION', 'Creación'),
        ('MODIFICACION', 'Modificación'),
        ('BAJA', 'Baja lógica'),
        ('PRESTAMO', 'Registro préstamo'),
        ('DEVOLUCION', 'Registro devolución'),
        ('RESERVA', 'Registro reserva'),
        ('CANCELACION', 'Cancelación'),
        ('SANCION', 'Aplicación sanción'),
        ('LOGIN', 'Inicio sesión'),
    )

    usuario_interno = models.ForeignKey(
        UsuarioInterno,
        on_delete=models.SET_NULL,
        null=True
    )

    accion = models.CharField(max_length=30, choices=ACCIONES)
    entidad = models.CharField(max_length=100)
    fecha = models.DateTimeField(default=timezone.now)
    detalle = models.TextField()

    ip_origen = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ['-fecha']
        indexes = [
            models.Index(fields=['fecha']),
            models.Index(fields=['accion']),
        ]

    def __str__(self):
        return f"{self.fecha} - {self.accion} - {self.entidad}"
