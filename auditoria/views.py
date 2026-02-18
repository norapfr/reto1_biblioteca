from django.shortcuts import render
from usuarios.decorators import rol_requerido
from .models import Auditoria


@rol_requerido(['ADMIN', 'DIRECCION'])
def lista_logs(request):

    accion = request.GET.get("accion")
    fecha_inicio = request.GET.get("inicio")
    fecha_fin = request.GET.get("fin")

    logs = Auditoria.objects.all()

    if accion:
        logs = logs.filter(accion=accion)

    if fecha_inicio and fecha_fin:
        logs = logs.filter(
            fecha__gte=fecha_inicio,
            fecha__lte=fecha_fin
        )

    return render(request, "auditoria/lista.html", {
        "logs": logs
    })
