from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_titulos, name='lista_titulos'),
    path('crear/', views.crear_titulo, name='crear_titulo'),
    path('detalle/<int:pk>/', views.detalle_titulo, name='detalle_titulo'),
    path('baja/<int:pk>/', views.baja_titulo, name='baja_titulo'),
]
