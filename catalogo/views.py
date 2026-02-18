from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Titulo, Ejemplar
from .forms import TituloForm, EjemplarForm
from .services import baja_logica_titulo, baja_logica_ejemplar
from auditoria.services import registrar_auditoria
from usuarios.decorators import rol_requerido


@rol_requerido(['ADMIN', 'PERSONAL'])
def lista_titulos(request):
    query = request.GET.get('q')

    if query:
        titulos = Titulo.objects.filter(
            Q(titulo__icontains=query) |
            Q(autor__icontains=query) |
            Q(isbn__icontains=query) |
            Q(categoria__icontains=query)
        )
    else:
        titulos = Titulo.objects.all()

    return render(request, 'catalogo/lista.html', {'titulos': titulos})


from .services import crear_ejemplar_multiple


@rol_requerido(['ADMIN', 'PERSONAL'])
def crear_titulo(request):

    if request.method == 'POST':
        form = TituloForm(request.POST)

        if form.is_valid():
            titulo = form.save()

            cantidad = form.cleaned_data['cantidad_ejemplares']

            # ✅ Crear ejemplares automáticamente
            crear_ejemplar_multiple(titulo, cantidad)

            registrar_auditoria(
                request,
                "CREACION",
                "Titulo",
                f"Título {titulo.isbn} con {cantidad} ejemplares"
            )

            messages.success(
                request,
                f"Título y {cantidad} ejemplares creados correctamente."
            )

            return redirect('lista_titulos')

    else:
        form = TituloForm()

    return render(request, 'catalogo/form_titulo.html', {'form': form})


@rol_requerido(['ADMIN', 'PERSONAL'])
def detalle_titulo(request, pk):
    titulo = get_object_or_404(Titulo, pk=pk)
    ejemplares = titulo.ejemplares.all()

    return render(request, 'catalogo/detalle.html', {
        'titulo': titulo,
        'ejemplares': ejemplares
    })


@rol_requerido(['ADMIN'])
def baja_titulo(request, pk):

    titulo = get_object_or_404(Titulo, pk=pk)

    # Baja lógica
    titulo.activo = False
    titulo.save()

    # Registrar auditoría
    registrar_auditoria(
        request,
        "BAJA",
        "Titulo",
        f"Baja lógica del título ISBN {titulo.isbn}"
    )

    messages.success(request, "Título dado de baja correctamente.")

    return redirect("lista_titulos")
