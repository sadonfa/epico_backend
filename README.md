# 🌍 Épico Viajes - Backend API

API REST desarrollada con **Django** y **Django REST Framework (DRF)** para la gestión de tours, categorías y reservas de la plataforma Épico Viajes.

---

## 🚀 Tecnologías y Herramientas
* **Python / Django 6.1** (Framework backend)
* **Django REST Framework** (Creación de endpoints API)
* **SimpleJWT** (Autenticación basada en JSON Web Tokens)
* **MySQL / SQLite** (Gestión de bases de datos)
* **Gunicorn & Nginx** (Despliegue en producción para VPS)

---

## ⚙️ Configuración del Entorno de Desarrollo (Local)

Sigue estos pasos para clonar y poner a marchar el proyecto en tu máquina local:

1. **Clona el repositorio:**
   ```bash
   git clone <url-de-tu-repositorio>
   cd epico_backend

2. **Crea y activa un entorno virtual:**
    ```python -m venv venv
    source venv/bin/activate  # En Linux/Mac
    # o ve\Scripts\activate en Windows``

3. **Instala las dependencias:**
    ```bash 
    pip install -r requirements.txt

4. **Configura tus variables de entorno:**
    Crea un archivo .env en la raíz del proyecto basado en la estructura segura y añade tus credenciales:
    ```SECRET_KEY=tu_clave_secreta
    DEBUG=True
    ALLOWED_HOSTS=localhost,127.0.0.1
    DB_NAME=tu_base_datos
    DB_USER=tu_usuario
    DB_PASSWORD=tu_contraseña
    DB_HOST=localhost
    DB_PORT=5432

5. **Aplica las migraciones y ejecuta el servidor:**
    ``bash
    python manage.py migrate
    python manage.py runserver