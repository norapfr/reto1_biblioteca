# Diseño Técnico y Propuesta Tecnológica (Versión Simple – Entorno Windows)
## Proyecto de Digitalización – Biblioteca Municipal “Rafael Alberti”

---

# 1. Enfoque General de la Solución

## 1.1 Tipo de Arquitectura

Se propone una **aplicación web monolítica modular**, accesible mediante navegador y desplegada en entorno Windows.

### Justificación

- El volumen de usuarios (8.000 socios y 4 usuarios internos) no requiere arquitectura distribuida.
- Presupuesto limitado → uso de tecnologías open source.
- Equipo técnico reducido → menor complejidad operativa.
- Fácil mantenimiento en entorno Windows, habitual en administraciones públicas.
- Cumple requisitos de integridad, trazabilidad y seguridad sin sobreingeniería.

La aplicación se organiza en módulos:

- Gestión de usuarios
- Catálogo
- Préstamos y devoluciones
- Reservas
- Sanciones
- Informes
- Auditoría

---

# 2. Componentes Principales

## 2.1 Backend

Aplicación web centralizada que gestiona:

- Lógica de negocio
- Validaciones
- Reglas de préstamo y sanción
- Control de acceso por roles
- Registro de auditoría
- Generación de informes

Toda la lógica reside en una única aplicación para simplificar mantenimiento.

---

## 2.2 Base de Datos

- Base de datos relacional centralizada.
- Restricciones de unicidad (DNI, ISBN).
- Claves foráneas para integridad.
- Índices en campos críticos.

Garantiza:

- Eliminación de duplicidades.
- Control de concurrencia.
- Trazabilidad estructurada.

---

## 2.3 Frontend

- Interfaz web accesible desde navegador (Chrome, Edge).
- Diseño simple y claro.
- Formularios con validaciones automáticas.
- Panel principal con accesos directos a:
  - Alta de socio
  - Nuevo préstamo
  - Devolución
  - Búsqueda de catálogo
  - Informes

No requiere instalación en los puestos de trabajo.

---

## 2.4 Infraestructura (Entorno Windows)

### Opción recomendada: Servidor Windows municipal

- Windows Server 2019 o superior.
- Aplicación desplegada como servicio Windows.
- Acceso desde red interna municipal.
- Certificado HTTPS instalado en el servidor.

Requisitos estimados:

- 4 vCPU
- 8 GB RAM
- 200 GB SSD

No se requiere clúster ni balanceador.

---

# 3. Modelo de Datos Básico

## 3.1 Entidades Principales

### Usuario
- id
- dni (único)
- nombre
- apellidos
- email
- telefono
- tipo_usuario
- activo
- fecha_alta
- fecha_baja

---

### Titulo
- id
- titulo
- autor
- isbn
- categoria

---

### Ejemplar
- id
- codigo_interno (único)
- titulo_id (FK)
- estado (Disponible / Prestado / Reservado / Bloqueado)

---

### Prestamo
- id
- usuario_id (FK)
- ejemplar_id (FK)
- fecha_inicio
- fecha_fin
- fecha_devolucion

---

### Reserva
- id
- usuario_id (FK)
- titulo_id (FK)
- fecha_reserva
- estado

---

### Sancion
- id
- usuario_id (FK)
- dias_sancion
- fecha_inicio
- fecha_fin
- activa

---

### Auditoria
- id
- usuario_interno
- accion
- entidad
- fecha
- detalle

---

## 3.2 Relaciones Clave

- Usuario 1:N Préstamo
- Usuario 1:N Reserva
- Usuario 1:N Sanción
- Título 1:N Ejemplar
- Ejemplar 1:N Préstamo
- Todas las operaciones críticas generan registro en Auditoría.

Modelo simple, normalizado y mantenible.

---

# 4. Propuesta Tecnológica Concreta (Windows)

## 4.1 Lenguaje

- Python 3.x

## 4.2 Framework

- Django

## 4.3 Base de Datos

- SQLlite que viene por defecto con Django

## 4.4 Servidor Web

- IIS (Internet Information Services) como servidor web
- wfastcgi para integración con Django

Alternativa sencilla:
- Ejecutar Django con Gunicorn bajo WSL si el departamento TI lo permite
- O servicio Windows con waitress (opción más simple)

---

## 4.5 Justificación

- Stack completamente open source.
- Compatible con entorno Windows.
- Sin necesidad de contenedores ni tecnologías complejas.
- Fácil mantenimiento por TI municipal.
- Amplia documentación y soporte.

---

# 5. Seguridad Básica Necesaria

## 5.1 Autenticación

- Usuario y contraseña individual.
- Gestión integrada en Django.
- Sesiones seguras.

---

## 5.2 Roles

- Administrador
- Personal biblioteca
- Dirección

Control de acceso basado en permisos por módulo.

---

## 5.3 Protección de Datos

- HTTPS obligatorio.
- Acceso restringido a red municipal.
- Registro de auditoría.
- Baja lógica de usuarios.
- Conservación de logs mínimo 5 años.
- Cumplimiento RGPD.

---

## 5.4 Copias de Seguridad


- Copia almacenada en servidor secundario o unidad de red.
- Retención 30 días.
- Pruebas periódicas de restauración.

---

# 6. Estrategia de Implantación Sencilla

## 6.1 Desarrollo

- Desarrollo en entorno Windows 10/11.
- Base de datos en servidor de pruebas.
- Control de versiones con Git.

---

## 6.2 Migración de Datos

1. Exportación desde Excel.
2. Limpieza y validación.
3. Script de carga inicial.
4. Validación por el personal.

---

## 6.3 Puesta en Producción

- Instalación en servidor Windows paralelo.
- Formación al personal.
- Prueba piloto.
- Cambio definitivo fuera de horario.
- Soporte inicial presencial.

---

## 6.4 Formación

- 6–8 horas prácticas.
- Manual básico de usuario.
- Procedimientos operativos definidos.

---

# Conclusión

La solución propuesta es una aplicación web monolítica desplegada en entorno Windows Server, basada en tecnologías open source y diseñada específicamente para:

- Reducir errores administrativos.
- Automatizar préstamos, reservas y sanciones.
- Garantizar integridad y trazabilidad.
- Cumplir normativa de protección de datos.
- Mantener bajo coste y simplicidad operativa.

El diseño es proporcional al alcance del proyecto, evita complejidad innecesaria y puede mantenerse fácilmente por el departamento TI municipal.
