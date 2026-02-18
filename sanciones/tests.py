from django.test import TestCase, Client
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import timedelta

from sanciones.models import Sancion
from sanciones.services import crear_sancion, actualizar_sanciones_vencidas
from usuarios.models import Socio


User = get_user_model()


# ======================================================
# MODELO
# ======================================================

class SancionModelTest(TestCase):

    def setUp(self):
        self.usuario = Socio.objects.create(
            dni="11111111A",
            nombre="Juan",
            apellidos="Pérez",
            email="juan@test.com",
            telefono="123456789",
            activo=True
        )

    def test_str(self):
        sancion = Sancion.objects.create(
            usuario=self.usuario,
            dias_sancion=5,
            fecha_inicio=timezone.now(),
            fecha_fin=timezone.now() + timedelta(days=5),
            activa=True
        )

        self.assertEqual(
            str(sancion),
            f"Sanción {self.usuario} - 5 días"
        )

    def test_verificar_estado_desactiva_si_vencida(self):
        sancion = Sancion.objects.create(
            usuario=self.usuario,
            dias_sancion=1,
            fecha_inicio=timezone.now() - timedelta(days=3),
            fecha_fin=timezone.now() - timedelta(days=1),
            activa=True
        )

        sancion.verificar_estado()
        sancion.refresh_from_db()

        self.assertFalse(sancion.activa)

    def test_verificar_estado_no_desactiva_si_no_vencida(self):
        sancion = Sancion.objects.create(
            usuario=self.usuario,
            dias_sancion=5,
            fecha_inicio=timezone.now(),
            fecha_fin=timezone.now() + timedelta(days=5),
            activa=True
        )

        sancion.verificar_estado()
        sancion.refresh_from_db()

        self.assertTrue(sancion.activa)


# ======================================================
# SERVICES
# ======================================================

class SancionServiceTest(TestCase):

    def setUp(self):
        self.usuario = Socio.objects.create(
            dni="22222222B",
            nombre="Ana",
            apellidos="Gómez",
            email="ana@test.com",
            telefono="987654321",
            activo=True
        )

    def test_crear_sancion_valida(self):
        sancion = crear_sancion(self.usuario, 3)

        self.assertIsNotNone(sancion)
        self.assertEqual(sancion.dias_sancion, 3)
        self.assertTrue(sancion.activa)

    def test_crear_sancion_dias_invalidos(self):
        sancion = crear_sancion(self.usuario, 0)
        self.assertIsNone(sancion)

    def test_actualizar_sanciones_vencidas(self):
        sancion = Sancion.objects.create(
            usuario=self.usuario,
            dias_sancion=1,
            fecha_inicio=timezone.now() - timedelta(days=5),
            fecha_fin=timezone.now() - timedelta(days=2),
            activa=True
        )

        actualizar_sanciones_vencidas()
        sancion.refresh_from_db()

        self.assertFalse(sancion.activa)


# ======================================================
# VISTAS
# ======================================================

class SancionViewsTest(TestCase):

    def setUp(self):
        self.client = Client()

        # Usuario interno con rol válido
        self.user = User.objects.create_user(
            username="admin",
            password="testpass",
            rol="ADMIN"
        )

        self.client.login(username="admin", password="testpass")

        self.usuario = Socio.objects.create(
            dni="33333333C",
            nombre="Luis",
            apellidos="Martínez",
            email="luis@test.com",
            telefono="555555555",
            activo=True
        )

        self.sancion = Sancion.objects.create(
            usuario=self.usuario,
            dias_sancion=5,
            fecha_inicio=timezone.now(),
            fecha_fin=timezone.now() + timedelta(days=5),
            activa=True
        )

    def test_lista_sanciones_view(self):
        response = self.client.get("/sanciones/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("sanciones", response.context)

    def test_sanciones_por_periodo_sin_filtro(self):
        response = self.client.get("/sanciones/periodo/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["sanciones"]), 1)

    def test_sanciones_por_periodo_con_filtro(self):
        fecha_inicio = timezone.now().date().isoformat()
        fecha_fin = (timezone.now() + timedelta(days=10)).date().isoformat()

        response = self.client.get(
            "/sanciones/periodo/",
            {
                "inicio": fecha_inicio,
                "fin": fecha_fin
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["sanciones"]), 1)
