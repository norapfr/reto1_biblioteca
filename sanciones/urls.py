from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_sanciones, name='lista_sanciones'),
    path('periodo/', views.sanciones_por_periodo, name='sanciones_periodo'),
]
