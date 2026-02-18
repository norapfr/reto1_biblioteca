from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Count
from prestamos.models import Prestamo
from sanciones.models import Sancion
from catalogo.models import Titulo
from usuarios.decorators import rol_requerido
from xhtml2pdf import pisa
from django.template.loader import render_to_string
import openpyxl
from datetime import datetime

from django.shortcuts import render
from usuarios.decorators import rol_requerido


@rol_requerido(['ADMIN', 'DIRECCION'])
def informes_home(request):
    return render(request, "informes/home.html")


@rol_requerido(['ADMIN', 'DIRECCION'])
def informe_mensual_prestamos(request):

    mes = request.GET.get("mes")
    año = request.GET.get("año")

    if not mes or not año:
        return render(request, "informes/seleccionar_mes.html")

    prestamos = Prestamo.objects.filter(
        fecha_inicio__month=mes,
        fecha_inicio__year=año
    )

    total = prestamos.count()

    context = {
        "prestamos": prestamos,
        "total": total,
        "mes": mes,
        "año": año
    }

    html = render_to_string("informes/pdf_prestamos.html", context)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=prestamos.pdf"
    pisa.CreatePDF(html, dest=response)
    return response


@rol_requerido(['ADMIN', 'DIRECCION'])
def exportar_excel_prestamos(request):

    mes = request.GET.get("mes")
    año = request.GET.get("año")

    prestamos = Prestamo.objects.filter(
        fecha_inicio__month=mes,
        fecha_inicio__year=año
    )

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Prestamos"

    ws.append(["Usuario", "Ejemplar", "Fecha Inicio", "Fecha Fin", "Devuelto"])

    for p in prestamos:
        ws.append([
            str(p.usuario),
            str(p.ejemplar),
            p.fecha_inicio.strftime("%d/%m/%Y"),
            p.fecha_fin.strftime("%d/%m/%Y"),
            "Sí" if p.fecha_devolucion else "No"
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = "attachment; filename=prestamos.xlsx"
    wb.save(response)
    return response


@rol_requerido(['ADMIN', 'DIRECCION'])
def estadisticas_catalogo(request):

    estadisticas = Titulo.objects.annotate(
        total_prestamos=Count('ejemplares__prestamos')
    ).order_by('-total_prestamos')

    return render(request, "informes/estadisticas.html", {
        "estadisticas": estadisticas
    })


@rol_requerido(['ADMIN', 'DIRECCION'])
def informe_sanciones(request):

    inicio = request.GET.get("inicio")
    fin = request.GET.get("fin")

    sanciones = Sancion.objects.all()

    if inicio and fin:
        sanciones = sanciones.filter(
            fecha_inicio__gte=inicio,
            fecha_fin__lte=fin
        )

    total = sanciones.count()

    return render(request, "informes/sanciones.html", {
        "sanciones": sanciones,
        "total": total
    })
