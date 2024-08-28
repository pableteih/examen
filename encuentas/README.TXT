SISTEMA DE ENCUESTAS CON DJANGO
================================

Este proyecto es un sistema de encuestas desarrollado con el framework Django. Permite a los usuarios crear encuestas, generar códigos para responderlas y ver las respuestas obtenidas.

REQUISITOS PREVIOS
------------------
- Python 3.12.2
- Django 5.1
- PostgreSQL

INSTALACIÓN
-----------


1. Crea y activa un entorno virtual:
    virtualenv env

2. Instala las dependencias necesarias:
    pip install -r requirements.txt


3. Configura la base de datos:
- Crea una base de datos PostgreSQL llamada `encuestas`.
- Ajusta los parámetros de conexión en el archivo `settings.py`:

    DATABASES = { 'default': { 'ENGINE': 'django.db.backends.postgresql',
                 'NAME': 'encuestas', 
                 'USER': 'tu_usuario',
                  'PASSWORD': 'tu_contraseña',
                   'HOST': 'localhost',
                    'PORT': '5432', } }

4. Aplica las migraciones para crear las tablas necesarias:

    python manage.py makemigrations 
    python manage.py migrate


5. Crea un superusuario para acceder al panel de administración de Django:

    python manage.py createsuperuser


6. Inicia el servidor de desarrollo:

    python manage.py runserver


USO DEL SISTEMA
---------------
1. **Crear Encuestas:**
- Accede al sitio web e inicia sesión.
- Dirígete a `/encuestas/crear/` para crear una nueva encuesta.

2. **Generar Códigos:**
- Después de crear una encuesta, navega a `/codigos/crear/<ID_ENCUESTA>/` para generar códigos para que los clientes puedan responder la encuesta.

3. **Responder Encuestas:**
- Los usuarios pueden ingresar un código en la página principal (`/`) para responder a una encuesta específica.

4. **Ver Respuestas:**
- Dirígete a `/respuestas/listar/<ID_PREGUNTA>/` para ver todas las respuestas asociadas a una pregunta específica.

DATOS DE USUARIOS
-----------------
- **Usuario Admin:**
- Nombre de usuario: `admin`
- Contraseña: `Admin1234`

- **Usuario Admin 2:**
- Nombre de usuario: `admin2`
- Contraseña: `admin2`








