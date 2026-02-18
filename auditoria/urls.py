from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_logs, name='lista_logs'),
]
