from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import IntegrityError

from .models import Titulo, Ejemplar
from .forms import TituloForm, EjemplarForm
from .services import crear_ejemplar_multiple


# =====================================================
# TESTS DE MODELOS
# =====================================================

class TituloModelTest(TestCase):

    def setUp(self):
        self.titulo = Titulo.objects.create(
            titulo="El Quijote",
            autor="Miguel de Cervantes",
            isbn="1234567890",
            categoria="Novela"
        )

    def test_creacion_titulo(self):
        """Verifica que el título se crea correctamente"""
        self.assertEqual(self.titulo.titulo, "El Quijote")
        self.assertTrue(self.titulo.activo)

    def test_isbn_unico(self):
        """No debe permitir duplicidad de ISBN"""
        with self.assertRaises(IntegrityError):
            Titulo.objects.create(
                titulo="Otro libro",
                autor="Autor",
                isbn="1234567890",  # mismo ISBN
                categoria="Ensayo"
            )


class EjemplarModelTest(TestCase):

    def setUp(self):
        self.titulo = Titulo.objects.create(
            titulo="1984",
            autor="George Orwell",
            isbn="999999999",
            categoria="Distopía"
        )

    def test_creacion_ejemplar(self):
        ejemplar = Ejemplar.objects.create(
            codigo_interno="999999999-1",
            titulo=self.titulo
        )
        self.assertEqual(ejemplar.estado, "DISPONIBLE")
        self.assertTrue(ejemplar.activo)


# =====================================================
# TESTS DE FORMULARIOS
# =====================================================

class TituloFormTest(TestCase):

    def test_form_valido(self):
        form = TituloForm(data={
            "titulo": "Libro Test",
            "autor": "Autor Test",
            "isbn": "555555",
            "categoria": "Test",
            "cantidad_ejemplares": 2
        })

        self.assertTrue(form.is_valid())

    def test_isbn_duplicado(self):
        Titulo.objects.create(
            titulo="Libro Existente",
            autor="Autor",
            isbn="111111",
            categoria="Test"
        )

        form = TituloForm(data={
            "titulo": "Libro Nuevo",
            "autor": "Autor Nuevo",
            "isbn": "111111",  # duplicado
            "categoria": "Test",
            "cantidad_ejemplares": 1
        })

        self.assertFalse(form.is_valid())
        self.assertIn("isbn", form.errors)


class EjemplarFormTest(TestCase):

    def setUp(self):
        self.titulo = Titulo.objects.create(
            titulo="Libro",
            autor="Autor",
            isbn="22222",
            categoria="Test"
        )

        Ejemplar.objects.create(
            codigo_interno="22222-1",
            titulo=self.titulo
        )

    def test_codigo_duplicado(self):
        form = EjemplarForm(data={
            "codigo_interno": "22222-1",  # ya existe
            "titulo": self.titulo.id
        })

        self.assertFalse(form.is_valid())
        self.assertIn("codigo_interno", form.errors)


# =====================================================
# TESTS DE SERVICIOS
# =====================================================

class ServiciosTest(TestCase):

    def setUp(self):
        self.titulo = Titulo.objects.create(
            titulo="Clean Code",
            autor="Robert C. Martin",
            isbn="33333",
            categoria="Programación"
        )

    def test_crear_ejemplares_multiples(self):
        ejemplares = crear_ejemplar_multiple(self.titulo, 3)

        self.assertEqual(len(ejemplares), 3)
        self.assertEqual(Ejemplar.objects.count(), 3)
        self.assertEqual(ejemplares[0].codigo_interno, "33333-1")


# =====================================================
# TESTS DE VISTAS
# =====================================================
from django.contrib.auth import get_user_model


class VistasTest(TestCase):

    def setUp(self):
        self.client = Client()

        User = get_user_model()

        self.user = User.objects.create_user(
            username="admin",
            password="admin123",
            rol="ADMIN"
        )

        self.client.login(username="admin", password="admin123")

        self.titulo = Titulo.objects.create(
            titulo="Django",
            autor="Autor Django",
            isbn="44444",
            categoria="Tecnología"
        )

    def test_lista_titulos(self):
        response = self.client.get(reverse("lista_titulos"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Django")

    def test_detalle_titulo(self):
        response = self.client.get(
            reverse("detalle_titulo", args=[self.titulo.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Autor Django")

    def test_crear_titulo_post(self):
        response = self.client.post(reverse("crear_titulo"), data={
            "titulo": "Nuevo Libro",
            "autor": "Nuevo Autor",
            "isbn": "77777",
            "categoria": "Test",
            "cantidad_ejemplares": 2
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Titulo.objects.filter(isbn="77777").count(), 1)
        self.assertEqual(Ejemplar.objects.filter(titulo__isbn="77777").count(), 2)
