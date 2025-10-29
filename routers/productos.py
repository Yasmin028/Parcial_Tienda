from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select, Session
from db import get_session
from models import Producto, Categoria
from schemas import ProductoCreate, ProductoRead, ProductoUpdate
from typing import Optional

router = APIRouter()


#  Crear producto
@router.post("/", response_model=ProductoRead, status_code=201, summary="Crear nuevo producto")
def crear_producto(producto: ProductoCreate, session: Session = Depends(get_session)):
    categoria = session.get(Categoria, producto.categoria_id)
    if not categoria:
        raise HTTPException(status_code=400, detail="La categoría asociada no existe.")
    
    
    existente = session.exec(select(Producto).where(Producto.nombre == producto.nombre)).first()
    if existente:
        raise HTTPException(status_code=409, detail="Ya existe un producto con ese nombre.")

    try:
        nuevo_producto = Producto(**producto.dict())
        session.add(nuevo_producto)
        session.commit()
        session.refresh(nuevo_producto) 
        return nuevo_producto
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear el producto: {e}")


#  Listar todos los productos
@router.get("/", response_model=list[ProductoRead], summary="Listar productos")
def listar_productos(session: Session = Depends(get_session)):
    productos = session.exec(select(Producto)).all()
    return productos


#  Buscar producto por ID o nombre
@router.get("/buscar", response_model=list[ProductoRead], summary="Buscar producto por ID o nombre")
def buscar_producto(
    id: Optional[int] = Query(default=None, description="ID del producto"),
    nombre: Optional[str] = Query(default=None, description="Nombre del producto"),
    session: Session = Depends(get_session)
):
    if not id and not nombre:
        raise HTTPException(status_code=400, detail="Debe proporcionar un ID o un nombre para la búsqueda.")

    query = select(Producto)
    if id:
        query = query.where(Producto.id == id)
    if nombre:
        query = query.where(Producto.nombre.ilike(f"%{nombre}%"))

    productos = session.exec(query).all()
    if not productos:
        raise HTTPException(status_code=404, detail="No se encontraron productos.")
    return productos


#  Actualizar producto
@router.put("/{producto_id}", response_model=ProductoRead, summary="Actualizar producto")
def actualizar_producto(producto_id: int, producto_update: ProductoUpdate, session: Session = Depends(get_session)):
    producto_db = session.get(Producto, producto_id)
    if not producto_db:
        raise HTTPException(status_code=404, detail="Producto no encontrado.")
    
    try:
        for key, value in producto_update.dict(exclude_unset=True).items():
            setattr(producto_db, key, value)
        session.add(producto_db)
        session.commit()
        session.refresh(producto_db)
        return producto_db
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar el producto: {e}")


# Eliminar producto
@router.delete("/{producto_id}", status_code=200, summary="Eliminar producto")
def eliminar_producto(producto_id: int, session: Session = Depends(get_session)):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado.")

    session.delete(producto)
    session.commit()
    return {"message": f"Producto '{producto.nombre}' eliminado correctamente."}
