# API RESTful con FastAPI, PyMySQL y Autenticación JWT para Gestión de Productos, Categorías y Usuarios

Este repositorio contiene el código fuente de una API RESTful desarrollada con el framework FastAPI de Python, utilizando PyMySQL para la conexión a una base de datos MySQL. La API ha sido extendida para proporcionar **funcionalidades de autenticación y autorización mediante JSON Web Tokens (JWT)**, además de las operaciones CRUD (Crear, Leer, Actualizar, Eliminar) para la gestión de productos, categorías y ahora, **usuarios**. El backend (API) se conecta a un frontend web (`web_view`) para la interacción con el usuario.

## Repositorio

El código fuente completo de este proyecto se encuentra en el siguiente repositorio de GitHub:

[https://github.com/JowelBB/CUL/tree/main/5TO/ZISVA-Electiva%20Disciplinar%20II%2025-1/Actividad_5](https://github.com/JowelBB/CUL/tree/main/5TO/ZISVA-Electiva%20Disciplinar%20II%2025-1/Actividad_5)

## Tecnologías Utilizadas

* **FastAPI:** Framework web moderno y de alto rendimiento para construir APIs con Python.
* **PyMySQL:** Driver de Python para conectar a servidores MySQL.
* **SQLAlchemy (ORM):** Toolkit de SQL y ORM (Object-Relational Mapper) para interactuar con la base de datos de manera programática.
* **python-jose:** Librería para la implementación de JSON Web Signatures (JWS) y JSON Web Encryption (JWE).
* **passlib:** Librería para el hashing seguro de contraseñas.
* **Python:** Lenguaje de programación principal.
* **HTML, CSS, JavaScript (Frontend):** Para la interfaz de usuario que consume la API.

## Arquitectura

El proyecto sigue una arquitectura básica cliente-servidor, con un enfoque en la seguridad:

* **Backend (API):** Desarrollado con FastAPI y PyMySQL/SQLAlchemy.
    * Expone endpoints RESTful para realizar operaciones CRUD en los datos de productos, categorías y usuarios almacenados en la base de datos MySQL.
    * **Implementa un sistema de autenticación y autorización basado en JWT.** Esto incluye endpoints para registro de usuarios, login, y protección de rutas que requieren un token de acceso válido.
    * La lógica de acceso a los datos y la gestión de usuarios se encuentran en los archivos `crud_productos.py`, `crud_categorias.py` y `crud_users.py`.
    * Los modelos de la base de datos están definidos en `models.py`, y la configuración de la base de datos en `db_config.py`.
    * La lógica de autenticación y hashing de contraseñas se gestiona en `auth.py`.
    * El archivo principal de la API es `main.py`.
* **Frontend (web_view):** Interfaz web que consume la API.
    * Desarrollada con HTML, CSS y JavaScript.
    * Gestiona el proceso de login y el almacenamiento del token JWT en el `localStorage` del navegador.
    * Envía el token JWT en los encabezados de las solicitudes a las rutas protegidas de la API.
    * Proporciona funcionalidades CRUD para productos y categorías.
    * Incluye un botón de "Cerrar Sesión" que elimina el token y redirige al usuario a la página de login, asegurando la finalización de la sesión.

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
    git clone [https://github.com/JowelBB/CUL.git](https://github.com/JowelBB/CUL.git)
    cd CUL/5TO/ZISVA-Electiva%20Disciplinar%20II%2025-1/Actividad_5
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
            username VARCHAR(255) NOT NULL UNIQUE,
            email VARCHAR(255) UNIQUE,
            full_name VARCHAR(255),
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


        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            full_name VARCHAR(55) NOT NULL,
            email VARCHAR(55) NOT NULL,
            username VARCHAR(55) NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            active TINYINT(1) NOT NULL DEFAULT 1
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

7.  **Accede a la aplicación Frontend:**
    * Abre el archivo `signup.html` en tu navegador web.
    * Podrás registrarte, iniciar sesión y navegar a `index.html` y `tables.html` una vez autenticado.
    * Recuerda que las rutas protegidas en el frontend ahora requieren que el token JWT esté presente en el `localStorage`.

8.  **Accede a la documentación de la API:**
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

* **`POST /productos/`:** **(PROTEGIDA)** Crea un nuevo producto.
* **`GET /productos/`:** Obtiene una lista de todos los productos.
* **`GET /productos/{product_id}`:** Obtiene un producto específico por su ID.
* **`PUT /productos/{product_id}`:** **(PROTEGIDA)** Actualiza un producto existente por su ID.
* **`DELETE /productos/{product_id}`:** **(PROTEGIDA)** Elimina un producto específico por su ID.

### Categorías

* **`POST /categorias/`:** **(PROTEGIDA)** Crea una nueva categoría.
* **`GET /categorias/`:** Obtiene una lista de todas las categorías.
* **`GET /categorias/{category_id}`:** Obtiene una categoría específica por su ID.
* **`PUT /categorias/{category_id}`:** **(PROTEGIDA)** Actualiza una categoría existente por su ID.
* **`DELETE /categorias/{category_id}`:** **(PROTEGIDA)** Elimina una categoría específica por su ID.

## Estructura del Código:

* CUL/
* └── 5TO/
* └── ZISVA-Electiva Disciplinar II 25-1/
* └── Actividad_5/  <-- Nueva carpeta para esta actividad
* ├── auth.py             # Lógica de autenticación JWT
* ├── db_config.py        # Configuración de la base de datos
* ├── main.py             # Archivo principal de la API (FastAPI)
* ├── models.py           # Definición de los modelos de la base de datos (SQLAlchemy)
* ├── recursos/
* │   ├── crud_categorias.py # Lógica CRUD para categorías
* │   ├── crud_productos.py  # Lógica CRUD para productos
* │   └── crud_users.py      # Lógica CRUD para usuarios
* ├── requirements.txt    # Lista de dependencias
* └── web_view/           # Archivos del frontend
* ├── signin.html     # Página de login
* ├── signup.html     # Página de registro
* ├── index.html      # Dashboard principal (protegido)
* └── tables.html     # Página de tablas (productos/categorías - protegido)
* └── style.css       # (Ejemplo, si tienes CSS externo)
* └── script.js       # (Ejemplo, si tienes JS externo)

## Consumo de la API desde el Frontend (`signin.html`, `index.html`, `tables.html`)

El frontend ahora consta de varias páginas HTML que interactúan con los endpoints de la API, **incluyendo la gestión de JWT para la autenticación**.

### Autenticación y Gestión de Sesión

* **`signin.html`**:
    * Maneja el envío de credenciales (`username`, `password`) al endpoint `POST /token` de la API.
    * Si la autenticación es exitosa, el token JWT (`access_token` y `token_type`) recibido se almacena en el `localStorage` del navegador.
    * El usuario es redirigido a `index.html` o `tables.html`.
* **`index.html` y `tables.html`**:
    * Al cargar estas páginas, se verifica la presencia del `access_token` en el `localStorage`. Si no existe, el usuario es redirigido a `login.html`.
    * Incluyen un botón "Cerrar Sesión" que, al ser clickeado, elimina el `access_token` y `token_type` del `localStorage` y redirige al usuario a `signin.html`, cerrando la sesión.

### Acceso a Rutas Protegidas

* Para acceder a los endpoints de la API marcados como **(PROTEGIDA)**, el JavaScript del frontend debe incluir el token JWT en el encabezado `Authorization` de cada solicitud `fetch` (o `XMLHttpRequest`). El formato es `Authorization: Bearer <your_access_token>`.
* Si una solicitud a una ruta protegida devuelve un error `401 Unauthorized` (debido a un token ausente, inválido o expirado), el frontend limpiará el token del `localStorage` y redirigirá al usuario a `login.html` para que vuelva a iniciar sesión.

### Operaciones CRUD (tables.html)

* **Listado de Productos y Categorías:** Se realizan peticiones `GET` (sin token) a `/productos/` y `/categorias/` para obtener las listas iniciales.
* **Creación, Actualización y Eliminación:** Las acciones de "Crear", "Actualizar" y "Eliminar" para productos y categorías (endpoints `POST`, `PUT`, `DELETE`) ahora requieren que el token JWT sea enviado en el encabezado `Authorization` para que la API las acepte.
* **Filtro y Controles:** La página `tables.html` incluye controles para filtrar por ID y realizar operaciones CRUD, con un margen adecuado entre el `select` y el botón "Enviar".

Este resumen proporciona una idea clara de cómo el frontend interactúa con los diferentes endpoints de la API, ahora con la capa de seguridad de JWT implementada, para realizar las operaciones CRUD y la gestión de sesión necesarias.
