from django.test import TestCase
from django.utils import timezone
from usuarios.models import Socio
from catalogo.models import Titulo, Ejemplar
from prestamos.models import Prestamo
from prestamos.services import crear_prestamo, registrar_devolucion
from sanciones.models import Sancion


class PrestamoServiceTest(TestCase):

    def setUp(self):
        """
        Se ejecuta antes de cada test.
        Creamos datos base reutilizables.
        """

        # Crear usuario activo
        self.usuario = Socio.objects.create(
            dni="12345678A",
            nombre="Juan",
            apellidos="Pérez",
            email="juan@test.com",
            telefono="600000000",
            tipo_usuario="ESTANDAR",
            activo=True
        )

        # Crear título
        self.titulo = Titulo.objects.create(
            titulo="Libro Test",
            autor="Autor Test",
            isbn="9781234567890",
            categoria="Ficción"
        )

        # Crear ejemplar disponible
        self.ejemplar = Ejemplar.objects.create(
            titulo=self.titulo,
            codigo_interno="EJ001",
            estado="DISPONIBLE"
        )

    # ✅ 1. PRÉSTAMO CORRECTO
    def test_crear_prestamo_exitoso(self):
        prestamo = crear_prestamo(self.usuario, self.ejemplar)

        self.assertIsNotNone(prestamo.id)
        self.assertEqual(prestamo.usuario, self.usuario)
        self.assertEqual(prestamo.ejemplar, self.ejemplar)

        # El ejemplar debe cambiar a PRESTADO
        self.ejemplar.refresh_from_db()
        self.assertEqual(self.ejemplar.estado, "PRESTADO")

    # ✅ 2. NO PERMITIR USUARIO INACTIVO
    def test_no_permitir_usuario_inactivo(self):
        self.usuario.activo = False
        self.usuario.save()

        with self.assertRaises(ValueError):
            crear_prestamo(self.usuario, self.ejemplar)

    # ✅ 3. NO PERMITIR PRÉSTAMO CON SANCIÓN ACTIVA
    def test_no_permitir_prestamo_con_sancion_activa(self):
        Sancion.objects.create(
            usuario=self.usuario,
            dias_sancion=5,
            fecha_inicio=timezone.now(),
            fecha_fin=timezone.now() + timezone.timedelta(days=5),
            activa=True
        )

        with self.assertRaises(ValueError):
            crear_prestamo(self.usuario, self.ejemplar)

    # ✅ 4. NO PERMITIR MÁS DE 3 PRÉSTAMOS ACTIVOS
    def test_no_superar_limite_prestamos(self):

        for i in range(3):
            ejemplar = Ejemplar.objects.create(
                titulo=self.titulo,
                codigo_interno=f"EJ00{i+2}",
                estado="DISPONIBLE"
            )
            crear_prestamo(self.usuario, ejemplar)

        nuevo_ejemplar = Ejemplar.objects.create(
            titulo=self.titulo,
            codigo_interno="EJ999",
            estado="DISPONIBLE"
        )

        with self.assertRaises(ValueError):
            crear_prestamo(self.usuario, nuevo_ejemplar)

    # ✅ 5. NO PERMITIR PRESTAR EJEMPLAR NO DISPONIBLE
    def test_no_prestar_ejemplar_no_disponible(self):
        self.ejemplar.estado = "PRESTADO"
        self.ejemplar.save()

        with self.assertRaises(ValueError):
            crear_prestamo(self.usuario, self.ejemplar)

    # ✅ 6. REGISTRAR DEVOLUCIÓN CORRECTAMENTE
    def test_registrar_devolucion_correcta(self):
        prestamo = crear_prestamo(self.usuario, self.ejemplar)

        retraso = registrar_devolucion(prestamo)

        self.assertEqual(retraso, 0)

        prestamo.refresh_from_db()
        self.assertIsNotNone(prestamo.fecha_devolucion)

        self.ejemplar.refresh_from_db()
        self.assertEqual(self.ejemplar.estado, "DISPONIBLE")

    # ✅ 7. GENERAR SANCIÓN SI HAY RETRASO
    def test_generar_sancion_por_retraso(self):
        prestamo = crear_prestamo(self.usuario, self.ejemplar)

        # Forzar fecha vencida
        prestamo.fecha_fin = timezone.now() - timezone.timedelta(days=5)
        prestamo.save()

        retraso = registrar_devolucion(prestamo)

        self.assertGreater(retraso, 0)

        sancion = Sancion.objects.filter(usuario=self.usuario).first()
        self.assertIsNotNone(sancion)
        self.assertTrue(sancion.activa)

    # ✅ 8. NO PERMITIR DEVOLVER DOS VECES
    def test_no_devolver_dos_veces(self):
        prestamo = crear_prestamo(self.usuario, self.ejemplar)
        registrar_devolucion(prestamo)

        with self.assertRaises(ValueError):
            registrar_devolucion(prestamo)
