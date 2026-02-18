from django.test import TestCase
from django.utils import timezone
from django.db import transaction
from usuarios.models import Socio
from catalogo.models import Titulo, Ejemplar
from reservas.models import Reserva
from reservas.services import (
    crear_reserva,
    asignar_ejemplar_disponible,
    cancelar_reserva
)


class ReservaServiceTest(TestCase):

    def setUp(self):
        """
        Se ejecuta antes de cada test.
        Creamos datos base reutilizables.
        """

        self.usuario_activo = Socio.objects.create(
            dni="12345678A",
            nombre="Juan",
            apellidos="Pérez",
            email="juan@test.com",
            telefono="600000000",
            activo=True
        )

        self.usuario_inactivo = Socio.objects.create(
            dni="87654321B",
            nombre="Ana",
            apellidos="López",
            email="ana@test.com",
            telefono="611111111",
            activo=False
        )

        self.titulo = Titulo.objects.create(
            titulo="El Quijote",
            autor="Cervantes",
            isbn="1234567890123",
            categoria="Novela"
        )

        self.ejemplar = Ejemplar.objects.create(
            codigo_interno="EJ001",
            titulo=self.titulo,
            estado="DISPONIBLE"
        )

    # ============================
    # TEST CREAR RESERVA
    # ============================

    def test_crear_reserva_correctamente(self):
        reserva = crear_reserva(self.usuario_activo, self.titulo)

        self.assertIsNotNone(reserva)
        self.assertEqual(reserva.estado, "ACTIVA")
        self.assertEqual(reserva.usuario, self.usuario_activo)
        self.assertEqual(reserva.titulo, self.titulo)

    def test_no_crear_reserva_usuario_inactivo(self):
        with self.assertRaises(ValueError):
            crear_reserva(self.usuario_inactivo, self.titulo)

    def test_no_permitir_reserva_duplicada(self):
        crear_reserva(self.usuario_activo, self.titulo)

        with self.assertRaises(ValueError):
            crear_reserva(self.usuario_activo, self.titulo)

    # ============================
    # TEST ASIGNACIÓN AUTOMÁTICA
    # ============================

    def test_asignar_ejemplar_disponible(self):
        reserva = crear_reserva(self.usuario_activo, self.titulo)

        ejemplar, reserva_actualizada = asignar_ejemplar_disponible(self.titulo)

        self.assertIsNotNone(ejemplar)
        self.assertEqual(ejemplar.estado, "RESERVADO")

        reserva.refresh_from_db()
        self.assertEqual(reserva.estado, "ATENDIDA")

    def test_no_asignar_si_no_hay_ejemplares(self):
        # Eliminamos ejemplar disponible
        self.ejemplar.delete()

        crear_reserva(self.usuario_activo, self.titulo)

        ejemplar, reserva = asignar_ejemplar_disponible(self.titulo)

        self.assertIsNone(ejemplar)
        self.assertIsNone(reserva)

    # ============================
    # TEST CANCELACIÓN
    # ============================

    def test_cancelar_reserva(self):
        reserva = crear_reserva(self.usuario_activo, self.titulo)

        cancelar_reserva(reserva)

        reserva.refresh_from_db()
        self.assertEqual(reserva.estado, "CANCELADA")

    # ============================
    # TEST ORDEN CRONOLÓGICO
    # ============================

    def test_reserva_se_atende_por_orden_cronologico(self):
        usuario2 = Socio.objects.create(
            dni="99999999C",
            nombre="Luis",
            apellidos="Martín",
            email="luis@test.com",
            telefono="622222222",
            activo=True
        )

        reserva1 = crear_reserva(self.usuario_activo, self.titulo)

        # Forzamos diferencia de tiempo
        reserva1.fecha_reserva = timezone.now()
        reserva1.save()

        reserva2 = crear_reserva(usuario2, self.titulo)

        ejemplar, reserva_atendida = asignar_ejemplar_disponible(self.titulo)

        self.assertEqual(reserva_atendida.id, reserva1.id)
