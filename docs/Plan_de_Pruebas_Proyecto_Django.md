# Plan de Pruebas para Proyecto Django

## 1. Objetivos Generales
- Verificar que cada módulo funcione correctamente según sus especificaciones.
- Garantizar la integridad de las operaciones CRUD en modelos.
- Comprobar la validación y comportamiento de formularios.
- Validar las vistas (views) tanto en sus respuestas HTTP como en el contenido que presentan.
- Testear la lógica de negocio implementada en módulos de servicios (services.py).
- Confirmar que las URLs resuelven correctamente y enlazan con las vistas adecuadas.
- Realizar pruebas de integración para flujos de usuario y funcionalidades completas.
- Validar la correcta generación y despliegue de las plantillas HTML.
- Asegurar la correcta gestión de autenticaciones/autorizaciones si aplica.
- Controlar la gestión de estados y reglas de negocio en préstamos, reservas, sanciones, etc.

## 2. Alcance de Pruebas por Aplicación

### Auditoría
- Test de modelos para registrar eventos y propiedades.
- Validar vistas que muestren logs de auditoría.
- Testear la correcta asignación de IP origen y acciones.

### Catálogo
- Pruebas de modelos que describen títulos y ejemplares.
- Validar formularios para creación/edición de títulos.
- Comprobar vistas de listar, detalle y formularios.
- Testear servicios relacionados con catálogo.

### Informes
- Verificar generación correcta de informes (estadísticas, pdf, etc).
- Testear vistas que permiten seleccionar períodos y muestran informes.
- Validar formatos y contenidos de salidas (HTML/PDF).

### Préstamos
- Probar modelos y lógica asociada a préstamos y devoluciones.
- Validar formularios de préstamos.
- Testear servicios (lógica de negocio) para gestión de préstamos.
- Verificar vistas de listado, vencidos y formularios.

### Reservas
- Validar modelos y estados de reserva.
- Testear formularios y procesos para realizar/cancelar reservas.
- Comprobar vistas de reservas y confirmaciones.
- Testear servicios de gestión de reservas.

### Sanciones
- Probar modelos de sanciones, períodos y estados.
- Validar vistas y plantillas relacionadas con sanciones.
- Asegurar que reglas de negocio se aplican correctamente.
- Testear servicios para aplicación y cálculo de sanciones.

### Usuarios
- Testear modelos de usuarios y perfiles.
- Validar formularios de creación, edición, baja de usuarios.
- Comprobar vistas de gestión de usuarios.
- Verificar mecanismos de autenticación/autorización si están implementados.

## 3. Tipos de Pruebas Recomendadas

### Pruebas Unitarias
- Probar métodos de modelos y funciones en services.py.
- Validación individual de formularios.

### Pruebas de Integración
- Flujos completos de uso que involucren varias apps, por ejemplo:
  - Crear usuario -> Reservar título -> Prestar ejemplar -> Gestionar sanción.
- Verificar interacción correcta entre vistas, modelos y servicios.

### Pruebas Funcionales / UI
- Validar que las páginas web cargan correctamente.
- Comprobar que formularios envían datos y muestran mensajes de error/exito.
- Verificar la navegación y enlaces.

### Pruebas de Rendimiento y Carga (Opcional)
- Si el sistema debe soportar muchos usuarios o datos.

## 4. Herramientas y Configuración
- Uso de pytest o unittest (según lo que incluya el proyecto) para ejecución de tests.
- Base de datos de test configurada para pruebas aisladas.
- Uso de fixtures o factories para datos iniciales.
- Cobertura de tests (coverage) para medir qué partes del código están cubiertas.

## 5. Organización y Ejecución de Pruebas
- Cada aplicación tendrá su módulo de tests (tests.py).
- Seguir convenciones Django para descubrimiento de tests.
- Automatizar ejecución periódica con CI/CD si se dispone.

## 6. Entregables del Plan de Pruebas
- Documentación del alcance y tipos de pruebas.
- Scripts y casos de prueba implementados en tests.py.
- Reportes de cobertura y resultados.
