# 📚 Sistema de Gestión Bibliotecaria  
## Biblioteca Municipal “Rafael Alberti”

---

# 1. Descripción del Proyecto

Este sistema es una aplicación web desarrollada en **Django (Python)** cuyo objetivo es digitalizar y centralizar la gestión administrativa de la Biblioteca Municipal “Rafael Alberti”.

La aplicación permite:

- Gestión de socios  
- Gestión de catálogo y ejemplares  
- Registro de préstamos y devoluciones  
- Gestión de reservas  
- Aplicación automática de sanciones  
- Generación de informes  
- Auditoría completa de operaciones  

El sistema está diseñado para:

- Reducir errores administrativos  
- Automatizar procesos manuales  
- Garantizar trazabilidad  
- Cumplir normativa RGPD  
- Funcionar en entorno Windows municipal  

---

# 2. Requisitos Previos

Antes de instalar el sistema, es necesario disponer de:

✅ Windows 10/11 o Windows Server  
✅ Python 3.10 o superior   
✅ Git instalado  

---

# 3. Instalación Paso a Paso

## 3.1 Clonar el repositorio

```bash
git clone https://github.com/norapfr/reto1_biblioteca.git
```

## 3.2 Crear entorno virtual

```bash
python -m venv venv
```

## 3.3 Activar entorno virtual

En Windows:

```bash
venv\Scripts\activate
```

## 3.4 Instalar dependencias 

```bash
pip install -r requirements.txt

```
---



# 4. Migraciones

Aplicar migraciones:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

# 5. Crear Usuario Administrador

```bash
python manage.py createsuperuser
```

Asignar:

- username  
- email  
- password  

Después asignar rol **ADMIN** desde el panel admin.

---

# 6. Ejecutar el Servidor

```bash
python manage.py runserver
```
Abrir navegador:
http://127.0.0.1:8000/