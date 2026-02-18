from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_reservas, name='lista_reservas'),
    path('nueva/', views.nueva_reserva, name='nueva_reserva'),
    path('cancelar/<int:pk>/', views.cancelar_reserva_view, name='cancelar_reserva'),
]
