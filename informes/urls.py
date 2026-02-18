from django.urls import path
from . import views

urlpatterns = [
    path('', views.informes_home, name='informes_home'),
    path('prestamos/pdf/', views.informe_mensual_prestamos, name='informe_prestamos_pdf'),
    path('prestamos/excel/', views.exportar_excel_prestamos, name='informe_prestamos_excel'),
    path('estadisticas/', views.estadisticas_catalogo, name='estadisticas_catalogo'),
    path('sanciones/', views.informe_sanciones, name='informe_sanciones'),
]
