from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from db import get_session
from models import Categoria
from schemas import CategoriaCreate, CategoriaRead, CategoriaUpdate

router = APIRouter()


@router.post("/", response_model=CategoriaRead, status_code=201, summary="Crear nueva categoría")
def crear_categoria(categoria: CategoriaCreate, session: Session = Depends(get_session)):
    # Verificar si ya existe una categoría con ese nombre
    existente = session.exec(select(Categoria).where(Categoria.nombre == categoria.nombre)).first()
    if existente:
        raise HTTPException(status_code=409, detail="Ya existe una categoría con ese nombre.")
    
    try:
        # Crear la categoría (el id se genera automáticamente si está definido en el modelo)
        nueva_categoria = Categoria(**categoria.dict())
        session.add(nueva_categoria)
        session.commit()
        session.refresh(nueva_categoria)  # Recupera el ID generado automáticamente
        return nueva_categoria
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear la categoría: {e}")


@router.get("/", response_model=list[CategoriaRead], summary="Listar categorías")
def listar_categorias(
    activas: bool = Query(default=True, description="Filtrar solo categorías activas"),
    session: Session = Depends(get_session)
):
    query = select(Categoria)
    if activas:
        query = query.where(Categoria.activo == True)
    categorias = session.exec(query).all()
    return categorias


@router.get("/buscar", response_model=CategoriaRead, summary="Buscar categoría por ID o nombre")
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


@router.put("/{id}", response_model=CategoriaRead, summary="Actualizar categoría")
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


@router.delete("/{id}", status_code=200, summary="Desactivar categoría")
def desactivar_categoria(id: int, session: Session = Depends(get_session)):
    categoria = session.get(Categoria, id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada.")
    
    categoria.activo = False
    session.add(categoria)
    session.commit()
    return {"message": f"Categoría '{categoria.nombre}' desactivada correctamente."}
