from django.db import models


class Titulo(models.Model):
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=255)
    isbn = models.CharField(max_length=20, unique=True)
    categoria = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=['isbn']),
            models.Index(fields=['titulo']),
            models.Index(fields=['autor']),
        ]

    def __str__(self):
        return f"{self.titulo} - {self.autor}"


class Ejemplar(models.Model):
    ESTADOS = (
        ('DISPONIBLE', 'Disponible'),
        ('PRESTADO', 'Prestado'),
        ('RESERVADO', 'Reservado'),
        ('BLOQUEADO', 'Bloqueado'),
    )

    codigo_interno = models.CharField(max_length=50, unique=True)
    titulo = models.ForeignKey(Titulo, on_delete=models.PROTECT, related_name="ejemplares")
    estado = models.CharField(max_length=20, choices=ESTADOS, default='DISPONIBLE')
    activo = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=['estado']),
        ]

    def __str__(self):
        return f"{self.codigo_interno} - {self.titulo.titulo}"
