from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_socios, name='lista_socios'),
    path('crear/', views.crear_socio, name='crear_socio'),
    path('baja/<int:pk>/', views.baja_socio, name='baja_socio'),
]
