from fastapi import FastAPI
from db import create_db_and_tables
from categorias import router as categorias_router
from productos import router as productos_router

app = FastAPI(
    title="API Tienda",
    description="API para gestionar categorías y productos con SQLModel y FastAPI.",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/", tags=["Inicio"])
def home():
    return {"message": "Bienvenido a la API de la Tienda"}

app.include_router(categorias_router, prefix="/categorias", tags=["Categorías"])
app.include_router(productos_router, prefix="/productos", tags=["Productos"])
