from fastapi import FastAPI
from db import create_db_and_tables
from routers import categorias, productos

app = FastAPI(
    title="API Tienda",
    description="API para gestionar categorías y productos con SQLModel y FastAPI.",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(categorias.router, prefix="/categorias", tags=["Categorías"])
app.include_router(productos.router, prefix="/productos", tags=["Productos"])

@app.get("/", tags=["Inicio"])
def home():
    return {"message": "Bienvenido a la API de la Tienda"}
