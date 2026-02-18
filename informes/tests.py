from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import datetime

from prestamos.models import Prestamo
from sanciones.models import Sancion
from catalogo.models import Titulo, Ejemplar
from usuarios.models import Socio


class InformesTest(TestCase):

    def setUp(self):
        self.client = Client()
        User = get_user_model()

        # ✅ Usuario interno (para login)
        self.admin = User.objects.create_user(
            username="admin",
            password="admin123",
            rol="ADMIN"
        )

        self.client.login(username="admin", password="admin123")

        # ✅ Crear SOCIO (usuario biblioteca)
        self.socio = Socio.objects.create(
            dni="12345678A",
            nombre="Juan",
            apellidos="Pérez",
            email="juan@test.com",
            telefono="600000000",
            activo=True
        )

        # ✅ Crear título y ejemplar
        self.titulo = Titulo.objects.create(
            titulo="Libro Test",
            autor="Autor Test",
            isbn="1234567890123",
            categoria="Ficción"
        )

        self.ejemplar = Ejemplar.objects.create(
            codigo_interno="EJ001",
            titulo=self.titulo,
            estado="Disponible"
        )

    # =========================================================
    # ✅ Acceso home informes
    # =========================================================

    def test_acceso_informes_home(self):
        response = self.client.get(reverse("informes_home"))
        self.assertEqual(response.status_code, 200)

    # =========================================================
    # ✅ PDF préstamos
    # =========================================================

    def test_generacion_pdf_prestamos(self):

        Prestamo.objects.create(
            usuario=self.socio,   # ✅ ahora es Socio
            ejemplar=self.ejemplar,
            fecha_inicio=datetime(2025, 1, 10),
            fecha_fin=datetime(2025, 1, 25)
        )

        response = self.client.get(reverse("informe_prestamos_pdf"), {
            "mes": 1,
            "año": 2025
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")

    # =========================================================
    # ✅ Excel préstamos
    # =========================================================

    def test_generacion_excel_prestamos(self):

        Prestamo.objects.create(
            usuario=self.socio,  # ✅ corregido
            ejemplar=self.ejemplar,
            fecha_inicio=datetime(2025, 1, 10),
            fecha_fin=datetime(2025, 1, 25)
        )

        response = self.client.get(reverse("informe_prestamos_excel"), {
            "mes": 1,
            "año": 2025
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["Content-Type"],
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # =========================================================
    # ✅ Estadísticas catálogo
    # =========================================================

    def test_estadisticas_catalogo(self):
        response = self.client.get(reverse("estadisticas_catalogo"))
        self.assertEqual(response.status_code, 200)

    # =========================================================
    # ✅ Informe sanciones con filtro
    # =========================================================

    def test_informe_sanciones_con_filtro(self):

        Sancion.objects.create(
            usuario=self.socio,  # ✅ corregido
            dias_sancion=5,
            fecha_inicio=datetime(2025, 1, 1),
            fecha_fin=datetime(2025, 1, 6),
            activa=False
        )

        response = self.client.get(reverse("informe_sanciones"), {
            "inicio": "2025-01-01",
            "fin": "2025-01-31"
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "5")
