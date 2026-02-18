from django.db import transaction
from django.utils import timezone
from .models import Reserva
from catalogo.models import Ejemplar


@transaction.atomic
def crear_reserva(usuario, titulo):

    if not usuario.activo:
        raise ValueError("Usuario inactivo.")

    # Evitar duplicidad de reserva activa
    if Reserva.objects.filter(
        usuario=usuario,
        titulo=titulo,
        estado='ACTIVA'
    ).exists():
        raise ValueError("Ya existe una reserva activa para este título.")

    reserva = Reserva.objects.create(
        usuario=usuario,
        titulo=titulo
    )

    return reserva


@transaction.atomic
def asignar_ejemplar_disponible(titulo):

    reserva = Reserva.objects.filter(
        titulo=titulo,
        estado='ACTIVA'
    ).order_by('fecha_reserva').first()

    ejemplar = Ejemplar.objects.filter(
        titulo=titulo,
        estado='DISPONIBLE'
    ).first()

    if reserva and ejemplar:
        ejemplar.estado = 'RESERVADO'
        ejemplar.save()

        reserva.estado = 'ATENDIDA'
        reserva.save()

        return ejemplar, reserva

    return None, None


def cancelar_reserva(reserva):
    reserva.estado = 'CANCELADA'
    reserva.save()
