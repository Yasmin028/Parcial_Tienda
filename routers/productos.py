from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select, Session
from db import get_session
from models import Producto, Categoria
from schemas import ProductoCreate, ProductoRead
from typing import Optional

router = APIRouter(prefix="/productos", tags=["Productos"])

# Crear producto
@router.post("/", response_model=ProductoRead)
def crear_producto(data: ProductoCreate, session: Session = Depends(get_session)):
    categoria = session.get(Categoria, data.categoria_id)
    if not categoria or not categoria.activa:
        raise HTTPException(status_code=404, detail="Categoría no válida")

    if data.stock < 0:
        raise HTTPException(status_code=400, detail="El stock no puede ser negativo")

    nuevo = Producto(**data.model_dump())
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)
    return nuevo

# Listar productos (con filtros)
@router.get("/", response_model=list[ProductoRead])
def listar_productos(
    categoria_id: Optional[int] = None,
    precio_min: Optional[float] = None,
    stock_min: Optional[int] = None,
    session: Session = Depends(get_session)
):
    statement = select(Producto).where(Producto.activo == True)
    if categoria_id:
        statement = statement.where(Producto.categoria_id == categoria_id)
    if precio_min is not None:
        statement = statement.where(Producto.precio >= precio_min)
    if stock_min is not None:
        statement = statement.where(Producto.stock >= stock_min)
    return session.exec(statement).all()

# Obtener producto
@router.get("/{producto_id}", response_model=ProductoRead)
def obtener_producto(producto_id: int, session: Session = Depends(get_session)):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

# Actualizar producto
@router.put("/{producto_id}", response_model=ProductoRead)
def actualizar_producto(producto_id: int, data: ProductoCreate, session: Session = Depends(get_session)):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    producto_data = data.model_dump(exclude_unset=True)
    for key, value in producto_data.items():
        setattr(producto, key, value)

    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto

# Desactivar producto
@router.patch("/{producto_id}/desactivar")
def desactivar_producto(producto_id: int, session: Session = Depends(get_session)):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    producto.activo = False
    session.add(producto)
    session.commit()
    return {"mensaje": "Producto desactivado correctamente"}

# Comprar producto (restar stock)
@router.post("/{producto_id}/comprar")
def comprar_producto(producto_id: int, cantidad: int = 1, session: Session = Depends(get_session)):
    producto = session.get(Producto, producto_id)
    if not producto or not producto.activo:
        raise HTTPException(status_code=404, detail="Producto no encontrado o inactivo")

    if producto.stock < cantidad:
        raise HTTPException(status_code=400, detail="Stock insuficiente")

    producto.stock -= cantidad
    session.add(producto)
    session.commit()
    return {"mensaje": "Compra exitosa", "stock_restante": producto.stock}
