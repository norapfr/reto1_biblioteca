from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Prestamo
from .forms import PrestamoForm
from .services import crear_prestamo, registrar_devolucion
from auditoria.services import registrar_auditoria
from usuarios.decorators import rol_requerido


@rol_requerido(['ADMIN', 'PERSONAL'])
def nuevo_prestamo(request):

    if request.method == "POST":
        form = PrestamoForm(request.POST)

        if form.is_valid():
            try:
                prestamo = crear_prestamo(
                    form.cleaned_data["usuario"],
                    form.cleaned_data["ejemplar"]
                )

                # ✅ IMPORTANTE: PASAR request, NO request.user.user
                registrar_auditoria(
                    request,
                    "PRESTAMO",
                    "Prestamo",
                    f"Préstamo ID {prestamo.id}"
                )

                messages.success(request, "Préstamo registrado correctamente.")
                return redirect("lista_prestamos")

            except ValueError as e:
                messages.error(request, str(e))

    else:
        form = PrestamoForm()

    return render(request, "prestamos/form.html", {"form": form})


@rol_requerido(['ADMIN', 'PERSONAL'])
def devolver_prestamo(request, pk):
    prestamo = get_object_or_404(Prestamo, pk=pk)

    try:
        retraso = registrar_devolucion(prestamo)

        registrar_auditoria(
            request,
            "DEVOLUCIÓN",
            "Prestamo",
            f"Préstamo ID {prestamo.id}"
        )

        if retraso > 0:
            crear_sancion(prestamo.usuario, retraso)
            messages.warning(request, f"Devolución con {retraso} días de retraso.")
        else:
            messages.success(request, "Devolución registrada correctamente.")

    except ValueError as e:
        messages.error(request, str(e))

    return redirect("lista_prestamos")


@rol_requerido(['ADMIN', 'PERSONAL'])
def lista_prestamos(request):
    prestamos = Prestamo.objects.all()
    return render(request, "prestamos/lista.html", {"prestamos": prestamos})


@rol_requerido(['ADMIN', 'PERSONAL'])
def prestamos_vencidos(request):
    from django.utils import timezone

    prestamos = Prestamo.objects.filter(
        fecha_devolucion__isnull=True,
        fecha_fin__lt=timezone.now()
    )

    return render(request, "prestamos/vencidos.html", {"prestamos": prestamos})
