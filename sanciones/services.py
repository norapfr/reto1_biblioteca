from django.utils import timezone
from django.db import transaction
from .models import Sancion


@transaction.atomic
def crear_sancion(usuario, dias_retraso):

    if dias_retraso <= 0:
        return None

    fecha_inicio = timezone.now()
    fecha_fin = fecha_inicio + timezone.timedelta(days=dias_retraso)

    sancion = Sancion.objects.create(
        usuario=usuario,
        dias_sancion=dias_retraso,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        activa=True
    )

    return sancion


def actualizar_sanciones_vencidas():
    """
    Método que puede ejecutarse periódicamente.
    """
    sanciones_activas = Sancion.objects.filter(activa=True)

    for sancion in sanciones_activas:
        sancion.verificar_estado()
