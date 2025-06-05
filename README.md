# API RESTful con FastAPI y PyMySQL para Gestión de Productos y Categorías

Este repositorio contiene el código fuente de una API RESTful desarrollada con el framework FastAPI de Python, utilizando PyMySQL para la conexión a una base de datos MySQL. La API proporciona funcionalidades CRUD (Crear, Leer, Actualizar, Eliminar) para la gestión de productos y categorías. El backend (API) se conecta a un frontend web (`web_view`) para la interacción con el usuario.

## Repositorio

El código fuente completo de este proyecto se encuentra en el siguiente repositorio de GitHub:

[https://github.com/JowelBB/CUL/tree/main/5TO/ZISVA-Electiva%20Disciplinar%20II%2025-1/Actividad_4](https://github.com/JowelBB/CUL/tree/main/5TO/ZISVA-Electiva%20Disciplinar%20II%2025-1/Actividad_4)

## Tecnologías Utilizadas

* **FastAPI:** Framework web moderno y de alto rendimiento para construir APIs con Python.
* **PyMySQL:** Driver de Python para conectar a servidores MySQL.
* **SQLAlchemy (ORM):** Toolkit de SQL y ORM (Object-Relational Mapper) para interactuar con la base de datos de manera programática.
* **Python:** Lenguaje de programación principal.

## Arquitectura

El proyecto sigue una arquitectura básica cliente-servidor:

* **Backend (API):** Desarrollado con FastAPI y PyMySQL/SQLAlchemy. Expone endpoints RESTful para realizar operaciones CRUD en los datos de productos y categorías almacenados en la base de datos MySQL. La lógica de acceso a los datos se encuentra en los archivos `crud_productos.py` y `crud_categorias.py`. Los modelos de la base de datos están definidos en `models.py`, y la configuración de la base de datos en `db_config.py`. El archivo principal de la API es `main.py`.
* **Frontend (web_view):** Existe una interfaz web que consume esta API. Desarrollada con HTML, CSS y JavaScript, realizando llamadas HTTP a los endpoints de la API para mostrar y manipular los datos.

## Requisitos Previos

Antes de ejecutar la API, asegúrate de tener instalado lo siguiente:

* **Python 3.7+:** Puedes descargarlo desde [https://www.python.org/downloads/](https://www.python.org/downloads/).
* **pip:** El gestor de paquetes de Python (generalmente incluido con la instalación de Python).
* **MySQL:** Un servidor de base de datos MySQL en ejecución.
* **PyMySQL:** (Se instalará con las dependencias del proyecto).
* **FastAPI:** (Se instalará con las dependencias del proyecto).
* **SQLAlchemy:** (Se instalará con las dependencias del proyecto).
* **uvicorn:** Un servidor ASGI para ejecutar la aplicación FastAPI.

## Instalación y Ejecución

Sigue estos pasos para configurar y ejecutar la API:

1.  **Clona el repositorio:**
    ```bash
    git clone [https://github.com/JowelBB/CUL/tree/main/5TO/ZISVA-Electiva%20Disciplinar%20II%2025-1/Actividad_4](https://github.com/JowelBB/CUL/tree/main/5TO/ZISVA-Electiva%20Disciplinar%20II%2025-1/Actividad_4)
    cd CUL/5TO/ZISVA-Electiva%20Disciplinar%20II%2025-1/Actividad_4
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
    *(Si no tienes un archivo `requirements.txt`, puedes crear uno con las dependencias necesarias: `fastapi`, `uvicorn[standard]`, `PyMySQL`, `SQLAlchemy`)*

4.  **Configura la conexión a la base de datos:**
    * Edita el archivo `db_config.py` para establecer los parámetros de conexión a tu servidor MySQL (host, usuario, contraseña, base de datos). Asegúrate de que la base de datos exista o que la API tenga permisos para crearla (según tu configuración).

5.  **Crea las tablas en la base de datos:**
    * Ejecuta el archivo `main.py`. Esto creará las tablas definidas en `models.py` si no existen:
        ```bash
        python main.py
        ```
        *(Nota: La API también intentará crear las tablas al inicio. Si prefieres un control más explícito, puedes ejecutar un script separado utilizando SQLAlchemy.)*
        
    * Crea una base de datos MySQL llamada `mi_api`.
    * Crea las tablas `productos` y `categorias` usando el siguiente script SQL:

        ```sql
        CREATE DATABASE mi_api;
        USE mi_api;

        CREATE TABLE categorias (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL
        );

        CREATE TABLE productos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            descripcion TEXT,
            precio DECIMAL(10, 2) NOT NULL,
            categoria_id INT,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id)
        );
        ```

    * Actualiza las credenciales de la base de datos en el archivo `db_config.py`:

        ```python
        "mysql+pymysql://tuusuario:tucontraseña@localhost:3306/mi_api"
        ```


6.  **Ejecuta la API con Uvicorn:**
    ```bash
    uvicorn main:app --reload
    ```
    * `main`: Es el nombre del archivo Python principal (sin la extensión `.py`).
    * `app`: Es el nombre de la instancia de FastAPI creada dentro de `main.py`.
    * `--reload`: Activa la recarga automática del servidor al detectar cambios en el código (útil para desarrollo).

7.  **Accede a la documentación de la API:**
    * Una vez que el servidor Uvicorn esté en ejecución, puedes acceder a la documentación interactiva de la API generada automáticamente por FastAPI en:
        * `http://127.0.0.1:8000/docs` (Swagger UI)
        * `http://127.0.0.1:8000/redoc` (ReDoc)

## Endpoints de la API

La API expone los siguientes endpoints para la gestión de productos y categorías:

### Productos

* **`POST /productos/`:** Crea un nuevo producto. Requiere un cuerpo JSON con los campos `name` (string), `description` (string), `price` (integer), y `categoria_id` (integer).
* **`GET /productos/`:** Obtiene una lista de todos los productos.
* **`GET /productos/{product_id}`:** Obtiene un producto específico por su ID.
* **`PUT /productos/{product_id}`:** Actualiza un producto existente por su ID. Requiere un cuerpo JSON con los campos a actualizar (`name`, `description`, `price`, `categoria_id`). Los campos son opcionales.
* **`DELETE /productos/{product_id}`:** Elimina un producto específico por su ID.

### Categorías

* **`POST /categorias/`:** Crea una nueva categoría. Requiere un cuerpo JSON con el campo `name` (string).
* **`GET /categorias/`:** Obtiene una lista de todas las categorías.
* **`GET /categorias/{category_id}`:** Obtiene una categoría específica por su ID.
* **`PUT /categorias/{category_id}`:** Actualiza una categoría existente por su ID. Requiere un cuerpo JSON con el campo `name` (string).
* **`DELETE /categorias/{category_id}`:** Elimina una categoría específica por su ID.

## Estructura del Código:

*    CUL/
*    └── 5TO/
*    └── ZISVA-Electiva Disciplinar II 25-1/
*    └── Actividad_4/
*    ├── db_config.py      # Configuración de la base de datos
*    ├── main.py           # Archivo principal de la API (FastAPI)
*    ├── models.py         # Definición de los modelos de la base de datos (SQLAlchemy)
*    ├── recursos/
*    │   ├── crud_categorias.py # Lógica CRUD para categorías
*    │   └── crud_productos.py  # Lógica CRUD para productos
*    └── requirements.txt  # (Opcional) Lista de dependencias

## Consumo de la API desde el Frontend (`Tablas.html`)

El frontend (`Tablas.html`) utiliza JavaScript y la librería jQuery para interactuar con los endpoints de esta API. A continuación, se describe cómo se consumen los diferentes endpoints:

### Listado de Productos y Categorías

* Al cargar la página, se realizan peticiones `GET` a `/productos/` y `/categorias/` para obtener la lista inicial de productos y categorías, respectivamente. Estos datos se utilizan para llenar las tablas en la interfaz de usuario.
* La función `cargarTabla()` es la encargada de realizar estas peticiones `GET` y actualizar el contenido de las tablas en el DOM.

### Creación de Productos y Categorías

* Al hacer clic en el botón "Guardar" dentro del modal de creación de productos, la función `crearProducto(data)` realiza una petición `POST` a `/productos/`. Los datos del nuevo producto (nombre, descripción, precio, categoría ID) se envían en el cuerpo de la solicitud como un objeto JSON (`application/json`).
* De manera similar, al guardar una nueva categoría, la función `crearCategoria(data)` realiza una petición `POST` a `/categorias/`, enviando el nombre de la categoría en el cuerpo de la solicitud como un objeto JSON (`application/json`).

### Obtención de Detalles para la Edición

* Al hacer clic en el botón "Actualizar" de un producto o categoría, se realiza una petición `GET` al endpoint específico (`/productos/{id}` o `/categorias/{id}`) para obtener los detalles del elemento a editar.
* Las funciones `cargarDatosProducto(id)` y `cargarDatosCategoria(id)` son responsables de realizar estas peticiones y de llenar los campos del modal de edición con la información recibida.

### Actualización de Productos y Categorías

* Al hacer clic en el botón "Guardar" dentro del modal de edición de productos, la función `actualizarProducto(id, data)` realiza una petición `PUT` al endpoint `/productos/{id}`. Los datos actualizados del producto se envían en el cuerpo de la solicitud como un objeto JSON (`application/json`).
* De forma análoga, al guardar los cambios en una categoría, la función `actualizarCategoria(id, data)` realiza una petición `PUT` a `/categorias/{id}`, enviando el nombre actualizado en el cuerpo de la solicitud como un objeto JSON (`application/json`).

### Eliminación de Productos y Categorías

* Al hacer clic en el botón "Eliminar" de un producto, la función `eliminarProducto(id)` realiza una petición `DELETE` al endpoint `/productos/{id}`.
* Del mismo modo, al eliminar una categoría, la función `eliminarCategoria(id)` realiza una petición `DELETE` al endpoint `/categorias/{id}`.

### Manejo de Respuestas

* Las funciones `success` dentro de las llamadas AJAX gestionan las respuestas exitosas de la API, mostrando mensajes de alerta al usuario y recargando las tablas para reflejar los cambios.
* Las funciones `error` gestionan las respuestas con errores de la API, mostrando mensajes de alerta con información sobre el fallo.

Este resumen proporciona una idea clara de cómo el frontend interactúa con los diferentes endpoints de la API para realizar las operaciones CRUD necesarias para la gestión de productos y categorías.
