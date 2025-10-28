from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select, Session
from db import get_session
from models import Producto, Categoria
from schemas import ProductoCreate, ProductoRead

router = APIRouter(prefix="/productos", tags=["Productos"])

@router.post("/", response_model=ProductoRead)
def crear_producto(data: ProductoCreate, session: Session = Depends(get_session)):
    categoria = session.get(Categoria, data.categoria_id)
    if not categoria or not categoria.activa:
        raise HTTPException(status_code=404, detail="Categoría no válida")
    if data.stock < 0:
        raise HTTPException(status_code=400, detail="Stock no puede ser negativo")
    nuevo = Producto(**data.model_dump())
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)
    return nuevo

@router.get("/", response_model=list[ProductoRead])
def listar_productos(session: Session = Depends(get_session)):
    return session.exec(select(Producto).where(Producto.activo == True)).all()

@router.get("/{producto_id}", response_model=ProductoRead)
def obtener_producto(producto_id: int, session: Session = Depends(get_session)):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.put("/{producto_id}", response_model=ProductoRead)
def actualizar_producto(producto_id: int, data: ProductoUpdate, session: Session = Depends(get_session)):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404)
    producto_data = data.model_dump(exclude_unset=True)
    for key, value in producto_data.items():
        setattr(producto, key, value)
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto
