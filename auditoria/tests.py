from django.test import TestCase, Client, RequestFactory
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import Auditoria
from .services import registrar_auditoria


class AuditoriaTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        User = get_user_model()

        self.user = User.objects.create_user(
            username="admin",
            password="admin123",
            rol="ADMIN"
        )

        self.client.login(username="admin", password="admin123")

    # =========================================================
    # ✅ RF-24 – Registro automático de operaciones críticas
    # =========================================================

    def test_registrar_auditoria_con_usuario_autenticado(self):
        """
        Verifica que se registre correctamente la auditoría
        cuando el usuario está autenticado.
        """

        request = self.factory.get("/")
        request.user = self.user
        request.META['REMOTE_ADDR'] = "127.0.0.1"

        registrar_auditoria(
            request=request,
            accion="LOGIN",
            entidad="Sistema",
            detalle="Inicio de sesión correcto"
        )

        self.assertEqual(Auditoria.objects.count(), 1)

        auditoria = Auditoria.objects.first()

        self.assertEqual(auditoria.usuario_interno, self.user)
        self.assertEqual(auditoria.accion, "LOGIN")
        self.assertEqual(auditoria.entidad, "Sistema")
        self.assertEqual(auditoria.ip_origen, "127.0.0.1")

    # =========================================================
    # ✅ Usuario no autenticado (debe guardar None)
    # =========================================================

    def test_registrar_auditoria_sin_usuario_autenticado(self):
        """
        Si el usuario no está autenticado,
        usuario_interno debe ser None.
        """

        request = self.factory.get("/")
        request.user = type("AnonymousUser", (), {"is_authenticated": False})()
        request.META['REMOTE_ADDR'] = "192.168.1.10"

        registrar_auditoria(
            request=request,
            accion="CREACION",
            entidad="Usuario",
            detalle="Intento creación usuario"
        )

        auditoria = Auditoria.objects.first()

        self.assertIsNone(auditoria.usuario_interno)
        self.assertEqual(auditoria.ip_origen, "192.168.1.10")

    # =========================================================
    # ✅ Validación ordering por fecha descendente
    # =========================================================

    def test_ordering_por_fecha_descendente(self):
        """
        Meta.ordering = ['-fecha']
        Debe devolver primero el registro más reciente.
        """

        Auditoria.objects.create(
            usuario_interno=self.user,
            accion="LOGIN",
            entidad="Sistema",
            detalle="Login 1",
            fecha=timezone.now()
        )

        Auditoria.objects.create(
            usuario_interno=self.user,
            accion="CREACION",
            entidad="Titulo",
            detalle="Creación libro",
            fecha=timezone.now() + timezone.timedelta(seconds=10)
        )

        auditorias = Auditoria.objects.all()

        self.assertEqual(auditorias[0].accion, "CREACION")
        self.assertEqual(auditorias[1].accion, "LOGIN")

    # =========================================================
    # ✅ Validación de ACCIONES (choices)
    # =========================================================

    def test_acciones_validas_en_choices(self):
        """
        Verifica que las acciones definidas en RULES
        estén correctamente configuradas.
        """

        acciones = [choice[0] for choice in Auditoria.ACCIONES]

        self.assertIn("CREACION", acciones)
        self.assertIn("MODIFICACION", acciones)
        self.assertIn("BAJA", acciones)
        self.assertIn("PRESTAMO", acciones)
        self.assertIn("DEVOLUCION", acciones)
        self.assertIn("RESERVA", acciones)
        self.assertIn("CANCELACION", acciones)
        self.assertIn("SANCION", acciones)
        self.assertIn("LOGIN", acciones)

    # =========================================================
    # ✅ Test método __str__
    # =========================================================

    def test_str_representation(self):
        """
        Verifica el formato:
        fecha - accion - entidad
        """

        auditoria = Auditoria.objects.create(
            usuario_interno=self.user,
            accion="LOGIN",
            entidad="Sistema",
            detalle="Inicio sesión"
        )

        resultado = str(auditoria)

        self.assertIn("LOGIN", resultado)
        self.assertIn("Sistema", resultado)
