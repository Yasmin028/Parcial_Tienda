from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from db import get_session
from models import Categoria, Producto
from schemas import CategoriaCreate, CategoriaRead, CategoriaUpdate, ProductoRead

router = APIRouter()


@router.post("/", response_model=CategoriaRead, status_code=201, summary="Crear nueva categoría")
def crear_categoria(categoria: CategoriaCreate, session: Session = Depends(get_session)):
    existente = session.exec(select(Categoria).where(Categoria.nombre == categoria.nombre)).first()
    if existente:
        raise HTTPException(status_code=409, detail="Ya existe una categoría con ese nombre.")
    
    nueva_categoria = Categoria(**categoria.dict())
    session.add(nueva_categoria)
    session.commit()
    session.refresh(nueva_categoria) 
    return nueva_categoria


@router.get("/", response_model=list[CategoriaRead])
def listar_categorias(
    activas: bool = Query(default=True, description="Filtrar solo categorías activas"),
    session: Session = Depends(get_session)
):
    query = select(Categoria)
    if activas:
        query = query.where(Categoria.activo == True)
    categorias = session.exec(query).all()
    return categorias



@router.get("/buscar", response_model=CategoriaRead)
def buscar_categoria(
    id: int | None = Query(default=None),
    nombre: str | None = Query(default=None),
    session: Session = Depends(get_session)
):
    if not id and not nombre:
        raise HTTPException(status_code=400, detail="Debe proporcionar un ID o un nombre para la búsqueda.")
    
    query = select(Categoria)
    if id:
        query = query.where(Categoria.id == id)
    elif nombre:
        query = query.where(Categoria.nombre.ilike(f"%{nombre}%"))
    
    categoria = session.exec(query).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada.")
    return categoria



@router.put("/{id}", response_model=CategoriaRead)
def actualizar_categoria(id: int, categoria_update: CategoriaUpdate, session: Session = Depends(get_session)):
    categoria = session.get(Categoria, id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada.")
    
    for key, value in categoria_update.dict(exclude_unset=True).items():
        setattr(categoria, key, value)
    
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria



@router.delete("/{id}", status_code=200)
def desactivar_categoria(id: int, session: Session = Depends(get_session)):
    categoria = session.get(Categoria, id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada.")

    categoria.activo = False
    productos = session.exec(select(Producto).where(Producto.categoria_id == id)).all()
    for p in productos:
        p.disponible = False
        session.add(p)
    session.add(categoria)
    session.commit()
    return {"message": f"Categoría '{categoria.nombre}' y sus productos fueron desactivados."}

@router.patch("/{categoria_id}/activar", status_code=200)
def activar_categoria(categoria_id: int, session: Session = Depends(get_session)):
    categoria = session.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    if categoria.activo:
        raise HTTPException(status_code=409, detail="La categoría ya está activa")
    categoria.activo = True
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return {"message": "Categoría activada correctamente"}

@router.get("/{categoria_id}/productos", response_model=list[ProductoRead])
def listar_productos_de_categoria(categoria_id: int, session: Session = Depends(get_session)):
    categoria = session.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada.")

    productos = session.exec(select(Producto).where(Producto.categoria_id == categoria_id)).all()
    return productos