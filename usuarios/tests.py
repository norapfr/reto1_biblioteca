from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.utils import timezone
from unittest.mock import patch

from .models import Socio
from .forms import SocioForm

UsuarioInterno = get_user_model()


# =====================================================
# 1️⃣ TESTS DE MODELO Socio
# =====================================================

class SocioModelTest(TestCase):

    def setUp(self):
        self.socio = Socio.objects.create(
            dni="12345678A",
            nombre="Juan",
            apellidos="Pérez",
            email="juan@example.com",
            telefono="600000000",
            tipo_usuario="ESTUDIANTE"
        )

    def test_creacion_socio_correcta(self):
        """RF-01: El socio debe crearse correctamente"""
        self.assertEqual(self.socio.dni, "12345678A")
        self.assertTrue(self.socio.activo)
        self.assertIsNotNone(self.socio.fecha_alta)

    def test_dni_unico(self):
        """RF-01: No se permite duplicidad por DNI"""
        with self.assertRaises(IntegrityError):
            Socio.objects.create(
                dni="12345678A",
                nombre="Pedro",
                apellidos="Gómez",
                email="pedro@example.com",
                telefono="611111111",
                tipo_usuario="GENERAL"
            )

    def test_baja_logica(self):
        """RF-04: La baja lógica debe desactivar el usuario"""
        self.socio.baja_logica()
        self.socio.refresh_from_db()

        self.assertFalse(self.socio.activo)
        self.assertIsNotNone(self.socio.fecha_baja)

    def test_str_representation(self):
        """El método __str__ debe mostrar nombre completo y DNI"""
        expected = "Juan Pérez - 12345678A"
        self.assertEqual(str(self.socio), expected)


# =====================================================
# 2️⃣ TESTS DE FORMULARIO SocioForm
# =====================================================

class SocioFormTest(TestCase):

    def setUp(self):
        Socio.objects.create(
            dni="11111111A",
            nombre="Ana",
            apellidos="López",
            email="ana@example.com",
            telefono="622222222",
            tipo_usuario="DOCENTE"
        )

    def test_form_valido(self):
        """El formulario debe ser válido con datos correctos"""
        form_data = {
            "dni": "22222222B",
            "nombre": "Carlos",
            "apellidos": "Ruiz",
            "email": "carlos@example.com",
            "telefono": "633333333",
            "tipo_usuario": "GENERAL"
        }

        form = SocioForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_dni_duplicado(self):
        """RF-01: Validación de DNI duplicado"""
        form_data = {
            "dni": "11111111A",
            "nombre": "Otro",
            "apellidos": "Usuario",
            "email": "otro@example.com",
            "telefono": "644444444",
            "tipo_usuario": "ESTUDIANTE"
        }

        form = SocioForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("dni", form.errors)


# =====================================================
# 3️⃣ TESTS DE VISTAS (SEGURIDAD + NEGOCIO)
# =====================================================

class SocioViewsTest(TestCase):

    def setUp(self):
        # Usuarios internos
        self.admin = UsuarioInterno.objects.create_user(
            username="admin",
            password="admin123",
            rol="ADMIN"
        )

        self.personal = UsuarioInterno.objects.create_user(
            username="personal",
            password="personal123",
            rol="PERSONAL"
        )

        self.direccion = UsuarioInterno.objects.create_user(
            username="direccion",
            password="direccion123",
            rol="DIRECCION"
        )

        # Socio existente
        self.socio = Socio.objects.create(
            dni="99999999Z",
            nombre="Laura",
            apellidos="Martínez",
            email="laura@example.com",
            telefono="655555555",
            tipo_usuario="GENERAL"
        )

    # -----------------------------------------
    # LOGIN Y CONTROL DE ACCESO
    # -----------------------------------------

    def test_lista_socios_requiere_login(self):
        """RNF-01: Requiere autenticación"""
        response = self.client.get(reverse("lista_socios"))
        self.assertEqual(response.status_code, 302)

    def test_lista_socios_con_permiso(self):
        """RNF-02: ADMIN puede acceder"""
        self.client.login(username="admin", password="admin123")
        response = self.client.get(reverse("lista_socios"))
        self.assertEqual(response.status_code, 200)

    def test_lista_socios_sin_permiso(self):
        """RNF-02: DIRECCION no puede acceder"""
        self.client.login(username="direccion", password="direccion123")
        response = self.client.get(reverse("lista_socios"))
        self.assertEqual(response.status_code, 302)

    # -----------------------------------------
    # CREACIÓN DE SOCIO
    # -----------------------------------------

    @patch("usuarios.views.registrar_auditoria")
    def test_crear_socio_post(self, mock_auditoria):
        """RF-01 + RF-24: Crear socio y registrar auditoría"""

        self.client.login(username="personal", password="personal123")

        data = {
            "dni": "88888888X",
            "nombre": "Nuevo",
            "apellidos": "Socio",
            "email": "nuevo@example.com",
            "telefono": "666666666",
            "tipo_usuario": "ESTUDIANTE"
        }

        response = self.client.post(reverse("crear_socio"), data)

        # Debe redirigir
        self.assertEqual(response.status_code, 302)

        # Debe existir en base de datos
        self.assertTrue(Socio.objects.filter(dni="88888888X").exists())

        # Debe haberse llamado auditoría
        mock_auditoria.assert_called_once()

    # -----------------------------------------
    # BAJA LÓGICA
    # -----------------------------------------

    @patch("usuarios.views.registrar_auditoria")
    def test_baja_socio(self, mock_auditoria):
        """RF-04: Baja lógica desde vista"""

        self.client.login(username="admin", password="admin123")

        response = self.client.post(
            reverse("baja_socio", args=[self.socio.pk])
        )

        self.assertEqual(response.status_code, 302)

        self.socio.refresh_from_db()
        self.assertFalse(self.socio.activo)

        mock_auditoria.assert_called_once()

    # -----------------------------------------
    # SUPERUSUARIO SIEMPRE PERMITIDO
    # -----------------------------------------

    def test_superusuario_acceso(self):
        """El superusuario siempre debe poder acceder"""

        superuser = UsuarioInterno.objects.create_superuser(
            username="super",
            password="super123",
            email="super@test.com",
            rol="ADMIN"
        )

        self.client.login(username="super", password="super123")

        response = self.client.get(reverse("lista_socios"))
        self.assertEqual(response.status_code, 200)
