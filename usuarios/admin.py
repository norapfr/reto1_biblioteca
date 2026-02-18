from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UsuarioInterno


@admin.register(UsuarioInterno)
class UsuarioInternoAdmin(UserAdmin):

    list_display = ("username", "email", "rol", "is_active", "is_staff")
    list_filter = ("rol", "is_active", "is_staff")
    search_fields = ("username", "email")
    ordering = ("username",)

    fieldsets = UserAdmin.fieldsets + (
        ("Información adicional", {
            "fields": ("rol",)
        }),
    )


from .models import Socio


@admin.register(Socio)
class SocioAdmin(admin.ModelAdmin):

    list_display = (
        "dni",
        "nombre",
        "apellidos",
        "email",
        "activo",
        "fecha_alta"
    )

    list_filter = ("activo",)
    search_fields = ("dni", "nombre", "apellidos", "email")
    ordering = ("apellidos",)

    readonly_fields = ("fecha_alta",)
