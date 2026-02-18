# Documento de Análisis Funcional y de Requisitos  
## Proyecto de Digitalización – Biblioteca Municipal “Rafael Alberti”

---

# 1. Descripción del Sistema Objetivo

## 1.1 Problema a Resolver

La Biblioteca Municipal “Rafael Alberti” gestiona actualmente sus procesos críticos (registro de socios, préstamos, devoluciones, reservas y sanciones) mediante herramientas manuales y hojas de cálculo independientes. Esta situación genera:

- Inconsistencias por edición simultánea.
- Pérdida y duplicidad de información.
- Errores en el orden de reservas.
- Cálculo manual e impreciso de sanciones.
- Incremento del tiempo de atención en mostrador.
- Dificultad para generar informes fiables.
- Sobrecarga administrativa que limita actividades culturales.

La ausencia de un sistema centralizado compromete la eficiencia operativa, la transparencia y la calidad del servicio al ciudadano.

---

## 1.2 Objetivos Específicos

1. Centralizar la información de usuarios, catálogo, préstamos y sanciones en un sistema único.
2. Automatizar los procesos de préstamo, devolución, reservas y cálculo de sanciones.
3. Garantizar la integridad y trazabilidad de la información.
4. Reducir al menos un 30% el tiempo medio de atención en mostrador en un plazo de 6 meses.
5. Facilitar la generación de informes fiables para la dirección y el Ayuntamiento.
6. Mejorar la experiencia del usuario mediante mayor transparencia y reducción de errores.

---

## 1.3 Alcance del Proyecto

### Incluye

- Implantación de un sistema integral de gestión bibliotecaria.
- Migración de datos históricos relevantes.
- Parametrización de reglas de negocio.
- Formación básica al personal.
- Implantación sin interrupción del servicio.

### No incluye

- Digitalización masiva de fondos físicos.
- Desarrollo de aplicaciones móviles nativas.
- Integraciones complejas con sistemas externos no municipales (salvo necesidad justificada).

---

## 1.4 Actores Involucrados

- Personal administrativo (4 usuarios internos).
- Dirección de la biblioteca.
- Usuarios/socios (8.000 activos).
- Departamento TI municipal.
- Proveedor adjudicatario.

---

# 2. Análisis de la Situación Actual (AS-IS)

## 2.1 Procesos Actuales

- Alta de socios mediante hojas de cálculo.
- Registro de préstamos en archivo compartido editable.
- Reservas anotadas en libreta física.
- Devoluciones verificadas manualmente.
- Cálculo manual de días de retraso y sanciones.
- Informes generados manualmente en Excel.

---

## 2.2 Problemas Identificados

- Edición concurrente sin control.
- Falta de integridad referencial.
- Ausencia de histórico estructurado.
- Duplicidad de registros.
- Reclamaciones por sanciones incorrectas.
- Dependencia del conocimiento individual del personal.

---

## 2.3 Impacto Operativo

- Aumento del tiempo medio de atención.
- Pérdida de confianza por parte de usuarios.
- Dificultad para planificación estratégica.
- Reducción de tiempo disponible para actividades culturales.

---

# 3. Modelo de Situación Futura (TO-BE)

## 3.1 Mejora de Procesos

- Registro único de usuarios con identificador inequívoco.
- Gestión transaccional de préstamos y devoluciones.
- Sistema automático de reservas con orden cronológico garantizado.
- Cálculo automático y parametrizable de sanciones.
- Generación automatizada de informes.

---

## 3.2 Cambios Organizativos

- Eliminación del uso de hojas de cálculo paralelas.
- Procedimientos operativos normalizados.
- Formación estructurada inicial.
- Definición formal de responsables funcionales.

---

## 3.3 Beneficios Esperados

- Reducción significativa de errores administrativos.
- Mejora de la trazabilidad.
- Mayor transparencia ante el ciudadano.
- Liberación de tiempo administrativo.
- Información fiable para toma de decisiones.

---

# 4. Requisitos Funcionales

## Módulo 1 – Gestión de Usuarios

**RF-01**  
El sistema permitirá registrar nuevos socios generando un identificador único.  
*Criterio de aceptación:* No se permiten duplicidades por DNI u otro identificador oficial.

**RF-02**  
Permitir la modificación de datos de usuario manteniendo histórico de cambios.

**RF-03**  
Permitir consulta completa del historial de préstamos, reservas y sanciones por usuario.

**RF-04**  
Permitir la baja lógica del usuario conservando el histórico asociado.

---

## Módulo 2 – Gestión de Catálogo

**RF-05**  
Alta, modificación y baja lógica de títulos y ejemplares.

**RF-06**  
Asociar múltiples ejemplares a un mismo título.

**RF-07**  
Consultar catálogo por título, autor, ISBN, categoría o estado.

**RF-08**  
Visualizar en tiempo real el estado del ejemplar (Disponible, Prestado, Reservado, Bloqueado).

---

## Módulo 3 – Préstamos y Devoluciones

**RF-09**  
Registrar préstamo asociando usuario, ejemplar y fecha.

**RF-10**  
Calcular automáticamente la fecha límite según tipo de usuario.

**RF-11**  
Bloquear préstamo si el usuario tiene sanción activa.

**RF-12**  
Registrar devolución y actualizar estado del ejemplar automáticamente.

**RF-13**  
Identificar préstamos vencidos mediante consulta o alerta interna.

---

## Módulo 4 – Reservas

**RF-14**  
Registrar reservas de ejemplares por orden cronológico automático.

**RF-15**  
Asignar automáticamente el ejemplar disponible al primer usuario en lista.

**RF-16**  
Permitir cancelación manual o automática tras periodo configurado.

---

## Módulo 5 – Sanciones

**RF-17**  
Calcular automáticamente días de retraso.

**RF-18**  
Aplicar sanción conforme a reglas parametrizadas.

**RF-19**  
Bloquear nuevos préstamos mientras exista sanción activa.

**RF-20**  
Mantener histórico completo de sanciones.

---

## Módulo 6 – Informes y Seguimiento

**RF-21**  
Generar informe mensual de préstamos exportable en PDF y Excel.

**RF-22**  
Generar estadísticas de uso del catálogo por periodo.

**RF-23**  
Generar informe de sanciones por periodo determinado.

---

## Módulo 7 – Auditoría

**RF-24**  
Registrar todas las operaciones críticas con fecha, hora y usuario interno.

**RF-25**  
Permitir consulta de logs por perfiles autorizados.

---

# 5. Requisitos No Funcionales

## Seguridad

- RNF-01: Autenticación obligatoria con credenciales individuales.
- RNF-02: Control de acceso basado en roles.
- RNF-03: Cifrado TLS 1.2 o superior.

## Protección de Datos

- RNF-04: Cumplimiento RGPD y normativa municipal.
- RNF-05: Registro de consentimiento cuando proceda.
- RNF-06: Posibilidad de anonimización tras baja definitiva.

## Rendimiento

- RNF-07: Tiempo de respuesta ≤ 2 segundos en operaciones estándar.
- RNF-08: Soporte mínimo de 10 usuarios concurrentes.

## Disponibilidad

- RNF-09: Disponibilidad mínima del 99% en horario de apertura.
- RNF-10: Mantenimiento fuera de horario de atención.

## Usabilidad

- RNF-11: Interfaz intuitiva adaptada a usuarios con conocimientos básicos.
- RNF-12: Formación necesaria ≤ 8 horas por usuario interno.

## Integridad

- RNF-13: Control de concurrencia en operaciones críticas.
- RNF-14: Validación obligatoria de campos clave.

## Auditoría

- RNF-15: Conservación de logs mínimo 5 años.

## Backup y Recuperación

- RNF-16: Copias de seguridad diarias automáticas.
- RNF-17: RTO ≤ 4 horas.
- RNF-18: RPO ≤ 24 horas.

## Compatibilidad Tecnológica

- RNF-19: Acceso vía navegador estándar actualizado.
- RNF-20: No requerir instalaciones complejas en puestos.

---

# 6. Reglas de Negocio

1. Máximo 3 ejemplares simultáneos por usuario estándar.
2. Duración estándar de préstamo: 15 días (parametrizable).
3. 1 día de suspensión por cada día de retraso.
4. Asignación de reservas por orden cronológico.
5. Usuario con sanción activa no puede realizar nuevos préstamos.

---

# 7. Restricciones

## Presupuestarias

- Solución ajustada a presupuesto municipal limitado.
- Prioridad a soluciones configurables frente a desarrollos a medida.

## Tecnológicas

- Infraestructura municipal existente.
- Nivel básico de competencia digital del personal.

## Normativas

- Cumplimiento RGPD y normativa municipal.

## Operativas

- No interrupción del servicio.
- Implantación progresiva.

---

# 8. Supuestos y Dependencias

- Disponibilidad del personal para formación.
- Colaboración del departamento TI municipal.
- Calidad mínima de datos históricos para migración.
- Validación jurídica previa.

---

# 9. Riesgos Identificados

| Riesgo | Impacto | Mitigación |
|--------|----------|------------|
| Resistencia al cambio | Medio | Formación y acompañamiento |
| Errores en migración | Alto | Pruebas piloto y validación |
| Incumplimiento normativo | Alto | Revisión legal previa |
| Subestimación del alcance | Medio | Validación formal del documento |
| Interrupción del servicio | Alto | Implantación escalonada |

---

# Conclusión

El presente análisis funcional establece una base estructurada y verificable para el diseño técnico e implantación de una solución integral de gestión bibliotecaria. Su correcta ejecución permitirá mejorar la eficiencia operativa, garantizar el cumplimiento normativo y ofrecer un servicio más ágil, transparente y fiable a la ciudadanía.
