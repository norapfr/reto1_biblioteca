from .models import Titulo, Ejemplar
from django.db import transaction


def baja_logica_titulo(titulo):
    titulo.activo = False
    titulo.save()


def baja_logica_ejemplar(ejemplar):
    ejemplar.activo = False
    ejemplar.save()


@transaction.atomic
def crear_ejemplar_multiple(titulo, cantidad):
    ejemplares = []
    for i in range(cantidad):
        codigo = f"{titulo.isbn}-{i+1}"
        ejemplares.append(
            Ejemplar.objects.create(
                codigo_interno=codigo,
                titulo=titulo
            )
        )
    return ejemplares
