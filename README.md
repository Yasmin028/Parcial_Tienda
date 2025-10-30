# 🏬 API Tienda — FastAPI + SQLModel

Esta es una API desarrollada con FastAPI y SQLModel para gestionar categorías y productos de una tienda online.  
Incluye validaciones, relaciones entre modelos, reglas de negocio y documentación interactiva con Swagger.

## 🚀 Características principales

- CRUD completo para categorías y productos
- Relación 1:N (una categoría tiene muchos productos)
- Validaciones con Pydantic
- Filtros avanzados en endpoints (stock, precio, categoría)
- Lógica de negocio implementada:
  - ✅ Nombre de categoría único  
  - ✅ Stock no puede ser negativo  
  - ✅ Cascada: desactivar categoría desactiva sus productos  
  - ✅ Compra reduce el stock automáticamente
- Documentación automática y funcional con Swagger UI

## ⚙️ Requisitos previos

Asegúrate de tener instalado:

- Python **3.10+**
- pip (gestor de paquetes)
- Git (para clonar el repositorio)

## 🧩 Instalación y configuración

1️⃣ Clonar el repositorio
git clone https://github.com/Yasmin028/Parcial_Tienda.git
cd Parcial_tienda

2️⃣ Crear entorno virtual
python -m venv venv
source venv/bin/activate

3️⃣ Instalar dependencias
pip install -r requirements.txt

▶️ Ejecución del servidor
fastapi dev
La API se ejecutará en:
http://127.0.0.1:8000/docs
Allí podrás probar todos los endpoints desde la interfaz de Swagger.


📚 Endpoints principales
🔹 Categorías
Método  	Endpoint	                    Descripción
POST    	/categorias/	                Crear nueva categoría
GET	      /categorias/	                Listar categorías activas
GET     	/categorias/buscar	          Buscar por ID o nombre
PUT	      /categorias/{id}            	Actualizar categoría
DELETE   	/categorias/{id}	            Desactivar categoría
PATCH	    /categorias/{id}/activar    	Reactivar categoría
GET	      /categorias/{id}/productos	  Listar productos de una categoría

## Productos
Método   	Endpoint                   Descripción
POST	    /productos/	               Crear nuevo producto
GET	      /productos/                Listar productos (filtros: stock, precio, categoría)
GET	      /productos/buscar          Buscar por ID o nombre
PUT	      /productos/{id}	           Actualizar producto
DELETE	  /productos/{id}	           Eliminar producto
POST	    /productos/{id}/comprar	   Comprar producto (reduce stock)

💡 Reglas de negocio
El nombre de la categoría debe ser único.
Stock y precio no pueden ser negativos.
Si una categoría se desactiva, sus productos también. 
Al comprar un producto, el stock disminuye automáticamente.

No se pueden registrar productos sin categoría válida.

🔍 Manejo de errores
Código	 Descripción	  Ejemplo
200	     OK	            Solicitud exitosa
201	     Created	      Categoría o producto creado
400	     Bad Request  	Datos inválidos o incompletos
404	     Not Found    	Recurso no encontrado
409	     Conflict	      Nombre duplicado o estado incompatible

🧰 Tecnologías utilizadas

FastAPI 

SQLModel

Pydantic

SQLite

Uvicorn

🧱 Estructura del proyecto
Tienda/
│
├── main.py
├── db.py
├── models.py
├── schemas.py
├── routers/
│   ├── categorias.py
│   └── productos.py
├── requirements.txt

🧾 Licencia

Proyecto de práctica académica — Libre para uso educativo y demostrativo.

Desarrollado por: Yasmin Velasco
Materia: Desarrollo de software
Profesor: Sergio Ivan Galvis
