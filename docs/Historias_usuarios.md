# Backlog de Producto  
## Proyecto de Digitalización – Biblioteca Municipal “Rafael Alberti”  
**Rol:** Product Owner Senior – Administración Pública  
**Trazabilidad:** Basado exclusivamente en los RF definidos en el documento de análisis funcional.

---

# 📦 MÓDULO 1 – GESTIÓN DE USUARIOS

---

## HU-01 – Alta de nuevo socio con identificador único  
**Requisitos:** RF-01  

### Historia  
Como personal administrativo  
Quiero registrar nuevos socios generando un identificador único  
Para garantizar la integridad de los datos y evitar duplicidades

### Descripción detallada  
El sistema permitirá crear un nuevo usuario solicitando los datos obligatorios (DNI u otro identificador oficial, nombre, apellidos, contacto, tipo de usuario, consentimiento RGPD si aplica).  
El sistema validará automáticamente que no exista otro usuario con el mismo identificador oficial.  
Se generará un identificador interno único no editable.

### Criterios de aceptación  

- Dado que intento registrar un usuario con un DNI ya existente  
  Cuando guardo el registro  
  Entonces el sistema impide el alta y muestra mensaje de duplicidad  

- Dado que los datos son válidos y no existen duplicidades  
  Cuando confirmo el alta  
  Entonces el sistema genera un identificador único y guarda el usuario  

### Reglas de negocio asociadas  
- No se permiten duplicidades por DNI (RF-01)

### Prioridad  
**Must**

### Dependencias  
RNF-02 (Control de acceso por roles)

### Consideraciones no funcionales  
- RNF-01 Autenticación obligatoria  
- RNF-04 Cumplimiento RGPD  
- RNF-14 Validación obligatoria de campos clave  
- RNF-15 Registro en auditoría  

---

## HU-02 – Modificación de datos de usuario con histórico  
**Requisitos:** RF-02  

### Historia  
Como personal administrativo  
Quiero modificar los datos de un socio manteniendo un histórico de cambios  
Para asegurar trazabilidad y cumplimiento normativo

### Descripción detallada  
El sistema permitirá editar datos personales no críticos.  
Cada modificación generará un registro de auditoría con fecha, hora y usuario interno que realizó el cambio.

### Criterios de aceptación  

- Dado que modifico datos de un usuario  
  Cuando guardo los cambios  
  Entonces el sistema registra el histórico con usuario, fecha y valores anteriores  

### Prioridad  
**Must**

### Dependencias  
HU-01  

### Consideraciones no funcionales  
- RNF-15 Conservación de logs 5 años  
- RNF-04 RGPD  

---

## HU-03 – Consulta integral del historial del usuario  
**Requisitos:** RF-03  

### Historia  
Como personal administrativo  
Quiero consultar el historial completo de préstamos, reservas y sanciones  
Para ofrecer atención precisa al usuario

### Criterios de aceptación  

- Dado que accedo a la ficha de un usuario  
  Cuando consulto su historial  
  Entonces visualizo préstamos activos, históricos, reservas y sanciones  

### Prioridad  
**Must**

### Dependencias  
HU-08, HU-14, HU-18  

### Consideraciones no funcionales  
- Tiempo de respuesta ≤ 2 segundos (RNF-07)

---

## HU-04 – Baja lógica de usuario  
**Requisitos:** RF-04  

### Historia  
Como personal administrativo  
Quiero dar de baja lógica a un usuario  
Para impedir nuevas operaciones manteniendo su histórico

### Criterios de aceptación  

- Dado que un usuario está activo  
  Cuando ejecuto la baja lógica  
  Entonces el usuario no puede realizar nuevos préstamos  
  Y su histórico permanece accesible  

### Prioridad  
**Must**

### Consideraciones no funcionales  
- RGPD (RNF-04, RNF-06)  

---

# 📚 MÓDULO 2 – GESTIÓN DE CATÁLOGO

---

## HU-05 – Alta y gestión de títulos y ejemplares  
**Requisitos:** RF-05, RF-06  

### Historia  
Como personal administrativo  
Quiero registrar títulos y asociar múltiples ejemplares  
Para gestionar correctamente el inventario

### Criterios de aceptación  

- Dado que creo un título  
  Cuando registro ejemplares asociados  
  Entonces el sistema permite múltiples ejemplares vinculados  

### Prioridad  
**Must**

### Consideraciones no funcionales  
- Integridad referencial (RNF-13)  

---

## HU-06 – Consulta avanzada de catálogo  
**Requisitos:** RF-07  

### Historia  
Como personal administrativo  
Quiero buscar títulos por múltiples criterios  
Para localizar rápidamente ejemplares

### Criterios de aceptación  

- Dado que introduzco un criterio (ISBN, autor, categoría)  
  Cuando ejecuto la búsqueda  
  Entonces el sistema devuelve resultados coincidentes  

### Prioridad  
**Must**

---

## HU-07 – Visualización del estado en tiempo real  
**Requisitos:** RF-08  

### Historia  
Como personal administrativo  
Quiero visualizar el estado actualizado del ejemplar  
Para informar correctamente al usuario

### Criterios de aceptación  

- Dado que consulto un ejemplar  
  Cuando accedo a su detalle  
  Entonces visualizo estado: Disponible, Prestado, Reservado o Bloqueado  

### Prioridad  
**Must**

---

# 🔄 MÓDULO 3 – PRÉSTAMOS Y DEVOLUCIONES

---

## HU-08 – Registro de préstamo  
**Requisitos:** RF-09, RF-10  

### Historia  
Como personal administrativo  
Quiero registrar un préstamo asociando usuario y ejemplar  
Para formalizar la cesión temporal del material

### Criterios de aceptación  

- Dado que el usuario no tiene sanción activa  
  Cuando registro el préstamo  
  Entonces se calcula automáticamente la fecha límite  

### Reglas de negocio  
- Máximo 3 ejemplares simultáneos  
- 15 días duración estándar  

### Prioridad  
**Must**

---

## HU-09 – Bloqueo por sanción activa  
**Requisitos:** RF-11  

### Historia  
Como sistema  
Quiero bloquear préstamos si existe sanción activa  
Para cumplir las reglas de negocio

### Criterios de aceptación  

- Dado que el usuario tiene sanción activa  
  Cuando intento registrar préstamo  
  Entonces el sistema lo impide  

### Prioridad  
**Must**

---

## HU-10 – Registro de devolución  
**Requisitos:** RF-12  

### Historia  
Como personal administrativo  
Quiero registrar devoluciones  
Para actualizar el estado del ejemplar

### Criterios de aceptación  

- Dado que registro devolución  
  Entonces el sistema cambia estado a Disponible  
  Y calcula retraso si aplica  

### Prioridad  
**Must**

---

## HU-11 – Identificación de préstamos vencidos  
**Requisitos:** RF-13  

### Historia  
Como personal administrativo  
Quiero consultar préstamos vencidos  
Para realizar seguimiento y reclamaciones

### Prioridad  
**Should**

---

# 📌 MÓDULO 4 – RESERVAS

---

## HU-12 – Registro de reserva cronológica  
**Requisitos:** RF-14  

### Historia  
Como personal administrativo  
Quiero registrar reservas por orden automático  
Para garantizar equidad

### Criterios de aceptación  

- Dado que dos usuarios reservan el mismo título  
  Entonces el sistema mantiene orden cronológico automático  

### Prioridad  
**Must**

---

## HU-13 – Asignación automática de ejemplar reservado  
**Requisitos:** RF-15  

### Historia  
Como sistema  
Quiero asignar automáticamente el ejemplar disponible al primero en lista  
Para respetar el orden de reserva  

### Prioridad  
**Must**

---

## HU-14 – Cancelación de reservas  
**Requisitos:** RF-16  

### Historia  
Como personal administrativo  
Quiero cancelar reservas manual o automáticamente  
Para mantener actualizada la lista

### Prioridad  
**Should**

---

# ⚖️ MÓDULO 5 – SANCIONES

---

## HU-15 – Cálculo automático de días de retraso  
**Requisitos:** RF-17  

### Historia  
Como sistema  
Quiero calcular automáticamente días de retraso  
Para aplicar sanciones correctas  

### Prioridad  
**Must**

---

## HU-16 – Aplicación automática de sanción  
**Requisitos:** RF-18  

### Historia  
Como sistema  
Quiero aplicar sanciones según reglas parametrizadas  
Para asegurar coherencia normativa  

### Reglas de negocio  
- 1 día de suspensión por día de retraso  

### Prioridad  
**Must**

---

## HU-17 – Histórico de sanciones  
**Requisitos:** RF-20  

### Historia  
Como personal administrativo  
Quiero consultar el histórico de sanciones  
Para atender reclamaciones  

### Prioridad  
**Must**

---

# 📊 MÓDULO 6 – INFORMES

---

## HU-18 – Informe mensual de préstamos  
**Requisitos:** RF-21  

### Historia  
Como dirección  
Quiero generar informe mensual exportable  
Para seguimiento institucional  

### Prioridad  
**Should**

---

## HU-19 – Estadísticas de uso del catálogo  
**Requisitos:** RF-22  

### Historia  
Como dirección  
Quiero obtener estadísticas por periodo  
Para planificación estratégica  

### Prioridad  
**Should**

---

## HU-20 – Informe de sanciones por periodo  
**Requisitos:** RF-23  

### Historia  
Como dirección  
Quiero generar informe de sanciones  
Para análisis de comportamiento  

### Prioridad  
**Should**

---

# 🔍 MÓDULO 7 – AUDITORÍA

---

## HU-21 – Registro automático de operaciones críticas  
**Requisitos:** RF-24  

### Historia  
Como sistema  
Quiero registrar todas las operaciones críticas  
Para garantizar trazabilidad y cumplimiento normativo  

### Prioridad  
**Must**

---

## HU-22 – Consulta de logs por perfiles autorizados  
**Requisitos:** RF-25  

### Historia  
Como usuario con perfil autorizado  
Quiero consultar registros de auditoría  
Para verificar operaciones realizadas  

### Prioridad  
**Should**


---
