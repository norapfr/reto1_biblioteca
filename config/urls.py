from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from usuarios.views import LoginPersonalizado
from config.views import dashboard,home
from usuarios.views import logout_personalizado

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuarios.urls')),
    path('catalogo/', include('catalogo.urls')),
    path('prestamos/', include('prestamos.urls')),
    path('reservas/', include('reservas.urls')),
    path('sanciones/', include('sanciones.urls')),
    path('informes/', include('informes.urls')),
    path('auditoria/', include('auditoria.urls')),

    
    path('logout/', logout_personalizado, name='logout'),

    path('login/', LoginPersonalizado.as_view(), name='login'),

    

    # Ruta principal
    path('', home, name='home'),

    # Dashboard protegido
    path('dashboard/', dashboard, name='dashboard'),


]
