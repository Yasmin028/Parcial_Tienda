from fastapi import FastAPI
from db import create_all_tables
from routers import categorias, productos

app = FastAPI(title="Tienda Online")

@app.on_event("startup")
def on_startup():
    create_all_tables()

app.include_router(categorias.router)
app.include_router(productos.router)
