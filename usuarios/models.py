from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class UsuarioInterno(AbstractUser):
    ROLES = (
        ('ADMIN', 'Administrador'),
        ('PERSONAL', 'Personal Biblioteca'),
        ('DIRECCION', 'Dirección'),
    )

    rol = models.CharField(max_length=20, choices=ROLES)

    def __str__(self):
        return f"{self.username} - {self.get_rol_display()}"


class Socio(models.Model):
    TIPOS = (
        ('ESTUDIANTE', 'Estudiante'),
        ('DOCENTE', 'Docente'),
        ('GENERAL', 'Público General'),
    )

    dni = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=150)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    tipo_usuario = models.CharField(max_length=20, choices=TIPOS)
    activo = models.BooleanField(default=True)
    fecha_alta = models.DateTimeField(default=timezone.now)
    fecha_baja = models.DateTimeField(null=True, blank=True)

    def baja_logica(self):
        self.activo = False
        self.fecha_baja = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.nombre} {self.apellidos} - {self.dni}"
