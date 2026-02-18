from django.db import models, transaction
from django.utils import timezone
from usuarios.models import Socio
from catalogo.models import Ejemplar
from sanciones.models import Sancion


class Prestamo(models.Model):
    usuario = models.ForeignKey(Socio, on_delete=models.PROTECT, related_name="prestamos")
    ejemplar = models.ForeignKey(Ejemplar, on_delete=models.PROTECT,related_name="prestamos")
    fecha_inicio = models.DateTimeField(default=timezone.now)
    fecha_fin = models.DateTimeField()
    fecha_devolucion = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['fecha_fin']),
        ]

    @classmethod
    def crear_prestamo(cls, usuario, ejemplar):
        with transaction.atomic():

            if not usuario.activo:
                raise ValueError("Usuario inactivo")

            if Sancion.objects.filter(usuario=usuario, activa=True).exists():
                raise ValueError("Usuario con sanción activa")

            prestamos_activos = cls.objects.filter(
                usuario=usuario,
                fecha_devolucion__isnull=True
            ).count()

            if prestamos_activos >= 3:
                raise ValueError("Máximo de préstamos alcanzado")

            if ejemplar.estado != 'DISPONIBLE':
                raise ValueError("Ejemplar no disponible")

            fecha_fin = timezone.now() + timezone.timedelta(days=15)

            prestamo = cls.objects.create(
                usuario=usuario,
                ejemplar=ejemplar,
                fecha_fin=fecha_fin
            )

            ejemplar.estado = 'PRESTADO'
            ejemplar.save()

            return prestamo

    def registrar_devolucion(self):
        if self.fecha_devolucion:
            raise ValueError("Ya devuelto")

        self.fecha_devolucion = timezone.now()
        self.save()

        self.ejemplar.estado = 'DISPONIBLE'
        self.ejemplar.save()

        retraso = (self.fecha_devolucion - self.fecha_fin).days

        if retraso > 0:
            from sanciones.models import Sancion
            Sancion.crear_sancion(self.usuario, retraso)
