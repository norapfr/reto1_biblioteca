from django.db import transaction
from django.utils import timezone
from .models import Prestamo
from sanciones.models import Sancion


DURACION_PRESTAMO_DIAS = 15
MAX_PRESTAMOS_ACTIVOS = 3


@transaction.atomic
def crear_prestamo(usuario, ejemplar):
    # 1. Validar usuario activo
    if not usuario.activo:
        raise ValueError("Usuario inactivo.")

    # 2. Validar sanción activa
    if Sancion.objects.filter(usuario=usuario, activa=True).exists():
        raise ValueError("El usuario tiene una sanción activa.")

    # 3. Validar límite de préstamos
    prestamos_activos = Prestamo.objects.filter(
        usuario=usuario,
        fecha_devolucion__isnull=True
    ).count()

    if prestamos_activos >= MAX_PRESTAMOS_ACTIVOS:
        raise ValueError("El usuario ya tiene el máximo de préstamos activos.")

    # 4. Validar estado del ejemplar
    if ejemplar.estado != "DISPONIBLE":
        raise ValueError("El ejemplar no está disponible.")

    # 5. Calcular fecha fin automática
    fecha_fin = timezone.now() + timezone.timedelta(days=DURACION_PRESTAMO_DIAS)

    # 6. Crear préstamo
    prestamo = Prestamo.objects.create(
        usuario=usuario,
        ejemplar=ejemplar,
        fecha_fin=fecha_fin
    )

    # 7. Actualizar estado ejemplar
    ejemplar.estado = "PRESTADO"
    ejemplar.save()

    return prestamo


@transaction.atomic
def registrar_devolucion(prestamo):
    if prestamo.fecha_devolucion:
        raise ValueError("El préstamo ya fue devuelto.")

    prestamo.fecha_devolucion = timezone.now()
    prestamo.save()

    # Cambiar estado del ejemplar
    ejemplar = prestamo.ejemplar
    ejemplar.estado = "DISPONIBLE"
    ejemplar.save()

    # Calcular retraso
    dias_diferencia = (prestamo.fecha_devolucion - prestamo.fecha_fin).days
    retraso = max(dias_diferencia, 0)

    if retraso > 0:
        from sanciones.services import crear_sancion
        crear_sancion(prestamo.usuario, retraso)

    return retraso
