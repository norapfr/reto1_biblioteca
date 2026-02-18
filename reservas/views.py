from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Reserva
from .forms import ReservaForm
from .services import crear_reserva, cancelar_reserva
from auditoria.services import registrar_auditoria
from usuarios.decorators import rol_requerido


@rol_requerido(['ADMIN', 'PERSONAL'])
def lista_reservas(request):
    reservas = Reserva.objects.all()
    return render(request, "reservas/lista.html", {"reservas": reservas})


@rol_requerido(['ADMIN', 'PERSONAL'])
def nueva_reserva(request):
    if request.method == "POST":
        form = ReservaForm(request.POST)
        if form.is_valid():
            try:
                reserva = crear_reserva(
                    form.cleaned_data['usuario'],
                    form.cleaned_data['titulo']
                )

                registrar_auditoria(
                    request,
                    "CREACIÓN",
                    "Reserva",
                    f"Reserva ID {reserva.id}"
                )

                messages.success(request, "Reserva registrada correctamente.")
                return redirect("lista_reservas")

            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = ReservaForm()

    return render(request, "reservas/form.html", {"form": form})


@rol_requerido(['ADMIN', 'PERSONAL'])
def cancelar_reserva_view(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)

    if request.method == "POST":
        cancelar_reserva(reserva)

        registrar_auditoria(
            request,
            "CANCELACION",
            "Reserva",
            f"Reserva ID {reserva.id}"
        )

        messages.success(request, "Reserva cancelada.")
        return redirect("lista_reservas")

    return render(request, "reservas/confirmar_cancelacion.html", {"reserva": reserva})

