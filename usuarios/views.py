from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Socio
from .forms import SocioForm
from .decorators import rol_requerido
from auditoria.services import registrar_auditoria
from django.contrib.auth import login


@rol_requerido(['ADMIN', 'PERSONAL'])
def lista_socios(request):
    socios = Socio.objects.all()
    return render(request, 'usuarios/lista.html', {'socios': socios})


@rol_requerido(['ADMIN', 'PERSONAL'])
def crear_socio(request):

    if request.method == 'POST':
        form = SocioForm(request.POST)

        if form.is_valid():
            socio = form.save()

            # ✅ Registrar auditoría
            registrar_auditoria(
                request,
                "CREACION",
                "Socio",
                f"Alta socio DNI {socio.dni}"
            )

            # ✅ Mensaje visual
            messages.success(
                request,
                "Socio creado correctamente."
            )

            # ✅ REDIRECCIÓN A LISTA
            return redirect('lista_socios')

        else:
            messages.error(
                request,
                "Error al crear el socio. Revise los datos."
            )

    else:
        form = SocioForm()

    return render(request, 'usuarios/form.html', {'form': form})


@rol_requerido(['ADMIN', 'PERSONAL'])
def baja_socio(request, pk):

    socio = get_object_or_404(Socio, pk=pk)

    if request.method == "POST":
        socio.activo = False
        socio.save()

        registrar_auditoria(
            request,
            "BAJA",
            "Socio",
            f"Baja lógica socio DNI {socio.dni}"
        )

        messages.success(request, "Socio dado de baja correctamente.")
        return redirect("lista_socios")

    return render(request, "usuarios/confirmar_baja.html", {"socio": socio})


from django.contrib.auth.views import LoginView


class LoginPersonalizado(LoginView):
    template_name = "login.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        registrar_auditoria(
            self.request,
            "LOGIN",
            "Sistema",
            "Inicio de sesión exitoso"
        )
        return response
from django.contrib.auth import logout
from django.shortcuts import redirect
from auditoria.services import registrar_auditoria


def logout_personalizado(request):
    if request.user.is_authenticated:
        registrar_auditoria(
            request,
            "LOGOUT",
            "Sistema",
            "Cierre de sesión"
        )

    logout(request)
    return redirect("login")
