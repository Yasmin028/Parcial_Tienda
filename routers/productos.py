# routers/productos.py
from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from db import engine
from models import Producto
from schemas import ProductoCreate, ProductoRead

router = APIRouter(prefix="/productos", tags=["Productos"])

@router.post("/", response_model=ProductoRead)
def crear_producto(producto: ProductoCreate):
    with Session(engine) as session:
        nuevo = Producto.from_orm(producto)
        session.add(nuevo)
        session.commit()
        session.refresh(nuevo)
        return nuevo

@router.get("/", response_model=list[ProductoRead])
def listar_productos():
    with Session(engine) as session:
        productos = session.exec(select(Producto)).all()
        return productos
