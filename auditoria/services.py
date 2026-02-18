from .models import Auditoria


def registrar_auditoria(request, accion, entidad, detalle):

    usuario = request.user if request.user.is_authenticated else None

    ip = request.META.get('REMOTE_ADDR')

    Auditoria.objects.create(
        usuario_interno=usuario,
        accion=accion,
        entidad=entidad,
        detalle=detalle,
        ip_origen=ip
    )
