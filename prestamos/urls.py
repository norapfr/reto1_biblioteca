from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_prestamos, name='lista_prestamos'),
    path('nuevo/', views.nuevo_prestamo, name='nuevo_prestamo'),
    path('devolver/<int:pk>/', views.devolver_prestamo, name='devolver_prestamo'),
    path('vencidos/', views.prestamos_vencidos, name='prestamos_vencidos'),
]
