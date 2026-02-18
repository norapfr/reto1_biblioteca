from django.shortcuts import redirect
from functools import wraps


def rol_requerido(roles_permitidos):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return redirect("login")

            # ✅ Permitir siempre al superusuario
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            # ✅ Validación por rol
            if request.user.rol not in roles_permitidos:
                return redirect("login")

            return view_func(request, *args, **kwargs)

        return _wrapped_view
    return decorator
