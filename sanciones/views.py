from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from usuarios.decorators import rol_requerido
from .models import Sancion
from django.utils import timezone


@login_required
@rol_requerido(['ADMIN', 'PERSONAL', 'DIRECCION'])
def lista_sanciones(request):

    actualizar_sanciones()

    sanciones = Sancion.objects.all()

    return render(request, "sanciones/lista.html", {
        "sanciones": sanciones
    })


@login_required
@rol_requerido(['ADMIN', 'DIRECCION'])
def sanciones_por_periodo(request):

    fecha_inicio = request.GET.get("inicio")
    fecha_fin = request.GET.get("fin")

    sanciones = Sancion.objects.all()

    if fecha_inicio and fecha_fin:
        sanciones = sanciones.filter(
            fecha_inicio__gte=fecha_inicio,
            fecha_fin__lte=fecha_fin
        )

    return render(request, "sanciones/periodo.html", {
        "sanciones": sanciones
    })


def actualizar_sanciones():
    from .services import actualizar_sanciones_vencidas
    actualizar_sanciones_vencidas()
