from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, Session
from db import get_session
from models import Producto, Categoria
from schemas import ProductoCreate, ProductoRead
from typing import Optional

router = APIRouter()

# Crear producto
@router.post("/", response_model=ProductoRead, status_code=201)
def crear_producto(producto: ProductoCreate, session: Session = Depends(get_session)):
    categoria = session.get(Categoria, producto.categoria_id)
    if not categoria:
        raise HTTPException(status_code=400, detail="La categoría asociada no existe.")
    
    db_producto = session.exec(select(Producto).where(Producto.nombre == producto.nombre)).first()
    if db_producto:
        raise HTTPException(status_code=409, detail="El producto ya existe.")

    nuevo_producto = Producto.from_orm(producto)
    session.add(nuevo_producto)
    session.commit()
    session.refresh(nuevo_producto)
    return nuevo_producto

# Listar todos
@router.get("/", response_model=list[ProductoRead])
def listar_productos(session: Session = Depends(get_session)):
    productos = session.exec(select(Producto)).all()
    return productos

# Buscar por ID o nombre
@router.get("/buscar", response_model=list[ProductoRead])
def buscar_producto(
    id: Optional[int] = None,
    nombre: Optional[str] = None,
    session: Session = Depends(get_session)
):
    """
    Busca productos por ID o nombre.
    """
    query = select(Producto)
    if id:
        query = query.where(Producto.id == id)
    if nombre:
        query = query.where(Producto.nombre.ilike(f"%{nombre}%"))

    productos = session.exec(query).all()
    if not productos:
        raise HTTPException(status_code=404, detail="No se encontraron productos.")
    return productos

# Actualizar producto
@router.put("/{producto_id}", response_model=ProductoRead)
def actualizar_producto(producto_id: int, producto: ProductoCreate, session: Session = Depends(get_session)):
    producto_db = session.get(Producto, producto_id)
    if not producto_db:
        raise HTTPException(status_code=404, detail="Producto no encontrado.")

    for key, value in producto.dict().items():
        setattr(producto_db, key, value)
    session.add(producto_db)
    session.commit()
    session.refresh(producto_db)
    return producto_db

# Eliminar producto
@router.delete("/{producto_id}", status_code=200)
def eliminar_producto(producto_id: int, session: Session = Depends(get_session)):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado.")
    session.delete(producto)
    session.commit()
    return {"message": "Producto eliminado correctamente."}
