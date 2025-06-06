# API RESTful con FastAPI, PyMySQL y Autenticación JWT

Este repositorio contiene el código fuente de una API RESTful desarrollada con el framework FastAPI de Python, utilizando PyMySQL para la conexión a una base de datos MySQL. La API proporciona funcionalidades de autenticación y autorización mediante JSON Web Tokens (JWT), además de las operaciones CRUD (Crear, Leer, Actualizar, Eliminar) para la gestión de productos, categorías y usuarios.

## Repositorio

El código fuente completo de este proyecto se encuentra en el siguiente repositorio de GitHub:

[https://github.com/JowelBB/Actividad_5_backend](https://github.com/JowelBB/Actividad_5_backend)

## Tecnologías Utilizadas

* **FastAPI:** Framework web moderno y de alto rendimiento para construir APIs con Python.
* **PyMySQL:** Driver de Python para conectar a servidores MySQL.
* **SQLAlchemy (ORM):** Toolkit de SQL y ORM (Object-Relational Mapper) para interactuar con la base de datos de manera programática.
* **python-jose:** Librería para la implementación de JSON Web Signatures (JWS) y JSON Web Encryption (JWE).
* **passlib:** Librería para el hashing seguro de contraseñas.
* **Python:** Lenguaje de programación principal.

## Arquitectura

Este repositorio se enfoca exclusivamente en el **backend (API)**, siguiendo una arquitectura orientada a la seguridad:

* Desarrollado con FastAPI y PyMySQL/SQLAlchemy.
* Expone endpoints RESTful para realizar operaciones CRUD en los datos de productos, categorías y usuarios almacenados en la base de datos MySQL.
* Implementa un sistema de autenticación y autorización basado en JWT. Esto incluye endpoints para registro de usuarios, login, y protección de rutas que requieren un token de acceso válido.
* La lógica de acceso a los datos y la gestión de usuarios se encuentran en los archivos `crud_productos.py`, `crud_categorias.py` y `crud_users.py` (dentro de la carpeta `recursos/`).
* Los modelos de la base de datos están definidos en `models.py`, y la configuración de la base de datos en `db_config.py`.
* La lógica de autenticación y hashing de contraseñas se gestiona en `auth.py`.
* El archivo principal de la API es `main.py`.

## Requisitos Previos

Antes de ejecutar la API, asegúrate de tener instalado lo siguiente:

* **Python 3.7+:** Puedes descargarlo desde [https://www.python.org/downloads/](https://www.python.org/downloads/).
* **pip:** El gestor de paquetes de Python (generalmente incluido con la instalación de Python).
* **MySQL:** Un servidor de base de datos MySQL en ejecución.
* **Dependencias de Python:** (Se instalarán con `requirements.txt`).

## Instalación y Ejecución

Sigue estos pasos para configurar y ejecutar la API:

1.  **Clona el repositorio:**
    ```bash
    git clone [https://github.com/JowelBB/Actividad_5_backend.git](https://github.com/JowelBB/Actividad_5_backend.git)
    cd Actividad_5_backend
    ```

2.  **Crea un entorno virtual (recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Linux/macOS
    venv\Scripts\activate  # En Windows
    ```

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Si no tienes un archivo `requirements.txt`, puedes crearlo con las dependencias necesarias: `fastapi`, `uvicorn[standard]`, `PyMySQL`, `SQLAlchemy`, `python-jose[cryptography]`, `passlib[bcrypt]`)*

4.  **Configura la conexión a la base de datos y JWT:**
    * Edita el archivo `db_config.py` para establecer los parámetros de conexión a tu servidor MySQL (host, usuario, contraseña, base de datos).
    * **Importante:** En `main.py` o un archivo de configuración separado, asegúrate de configurar tu `SECRET_KEY` para JWT. Genera una clave aleatoria y segura.

5.  **Crea la base de datos y las tablas:**
    * Asegúrate de que el usuario de MySQL tenga permisos para crear bases de datos y tablas, o créalas manualmente.
    * Crea una base de datos MySQL llamada `mi_api`.
    * Crea las tablas `users`, `productos` y `categorias` usando el siguiente script SQL:

        ```sql
        CREATE DATABASE IF NOT EXISTS mi_api;
        USE mi_api;

        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(55) NOT NULL UNIQUE,
            email VARCHAR(55) UNIQUE,
            full_name VARCHAR(55),
            hashed_password VARCHAR(255) NOT NULL,
            disabled BOOLEAN DEFAULT FALSE
        );

        CREATE TABLE IF NOT EXISTS categorias (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS productos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            descripcion TEXT,
            precio DECIMAL(10, 2) NOT NULL,
            categoria_id INT,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE SET NULL
        );
        ```

    * Actualiza las credenciales de la base de datos en el archivo `db_config.py` si es necesario:

        ```python
        # Ejemplo en db_config.py
        DATABASE_URL = "mysql+pymysql://tuusuario:tucontraseña@localhost:3306/mi_api"
        ```

6.  **Ejecuta la API con Uvicorn:**
    ```bash
    uvicorn main:app --reload
    ```
    * `main`: Es el nombre del archivo Python principal (sin la extensión `.py`).
    * `app`: Es el nombre de la instancia de FastAPI creada dentro de `main.py`.
    * `--reload`: Activa la recarga automática del servidor al detectar cambios en el código (útil para desarrollo).
    * **Para producción, se recomienda no usar `--reload` y considerar un servidor ASGI más robusto como Gunicorn con Uvicorn workers.**

7.  **Accede a la documentación de la API:**
    * Una vez que el servidor Uvicorn esté en ejecución, puedes acceder a la documentación interactiva de la API generada automáticamente por FastAPI en:
        * `http://127.0.0.1:8000/docs` (Swagger UI)
        * `http://127.0.0.1:8000/redoc` (ReDoc)

## Endpoints de la API

La API expone los siguientes endpoints para la gestión de productos, categorías y usuarios, **con rutas protegidas marcadas**:

### Autenticación y Usuarios

* **`POST /token`:** Obtiene un token de acceso JWT. Requiere `username` y `password` (form-data).
* **`POST /users/`:** Registra un nuevo usuario. Requiere un cuerpo JSON con `username`, `email`, `full_name` (opcional) y `password`.
* **`GET /users/me`:** **(PROTEGIDA)** Obtiene la información del usuario actual (basado en el token JWT proporcionado).

### Productos

* **`POST /productos/`:** **(PROTEGIDA)** Crea un nuevo producto. Requiere un cuerpo JSON con los campos `name` (string), `description` (string), `price` (float), y `categoria_id` (integer).
* **`GET /productos/`:** Obtiene una lista de todos los productos.
* **`GET /productos/{product_id}`:** Obtiene un producto específico por su ID.
* **`PUT /productos/{product_id}`:** **(PROTEGIDA)** Actualiza un producto existente por su ID. Requiere un cuerpo JSON con los campos a actualizar (`name`, `description`, `price`, `categoria_id`). Los campos son opcionales.
* **`DELETE /productos/{product_id}`:** **(PROTEGIDA)** Elimina un producto específico por su ID.

### Categorías

* **`POST /categorias/`:** **(PROTEGIDA)** Crea una nueva categoría. Requiere un cuerpo JSON con el campo `name` (string).
* **`GET /categorias/`:** Obtiene una lista de todas las categorías.
* **`GET /categorias/{category_id}`:** Obtiene una categoría específica por su ID.
* **`PUT /categorias/{category_id}`:** **(PROTEGIDA)** Actualiza una categoría existente por su ID. Requiere un cuerpo JSON con el campo `name` (string).
* **`DELETE /categorias/{category_id}`:** **(PROTEGIDA)** Elimina una categoría específica por su ID.

## Estructura del Código:

* Actividad_5_backend/
* ├── auth.py             # Lógica de autenticación JWT
* ├── db_config.py        # Configuración de la base de datos
* ├── main.py             # Archivo principal de la API (FastAPI)
* ├── models.py           # Definición de los modelos de la base de datos (SQLAlchemy)
* ├── recursos/
* │   ├── crud_categorias.py # Lógica CRUD para categorías
* │   ├── crud_productos.py  # Lógica CRUD para productos
* │   └── crud_users.py      # Lógica CRUD para usuarios
* └── requirements.txt    # Lista de dependencias
