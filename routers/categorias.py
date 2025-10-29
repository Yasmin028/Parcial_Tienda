# routers/categorias.py
from fastapi import APIRouter, HTTPException, Query
from sqlmodel import Session, select
from db import get_session
from models import Categoria
from schemas import CategoriaCreate, CategoriaRead, CategoriaUpdate

router = APIRouter()

# 🔹 Crear categoría
@router.post("/", response_model=CategoriaRead, status_code=201)
def crear_categoria(categoria: CategoriaCreate, session: Session = get_session()):
    # Validar nombre único
    existente = session.exec(select(Categoria).where(Categoria.nombre == categoria.nombre)).first()
    if existente:
        raise HTTPException(status_code=409, detail="Ya existe una categoría con ese nombre.")
    
    nueva_categoria = Categoria.from_orm(categoria)
    session.add(nueva_categoria)
    session.commit()
    session.refresh(nueva_categoria)
    return nueva_categoria


# 🔹 Listar categorías (solo las activas o todas)
@router.get("/", response_model=list[CategoriaRead])
def listar_categorias(
    session: Session = get_session(),
    activas: bool = Query(default=True, description="Filtrar solo categorías activas")
):
    query = select(Categoria)
    if activas:
        query = query.where(Categoria.activo == True)
    categorias = session.exec(query).all()
    return categorias


# 🔹 Obtener categoría por ID o nombre
@router.get("/buscar", response_model=CategoriaRead)
def obtener_categoria(
    id: int | None = Query(default=None, description="Buscar por ID"),
    nombre: str | None = Query(default=None, description="Buscar por nombre"),
    session: Session = get_session()
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


# 🔹 Actualizar categoría
@router.put("/{id}", response_model=CategoriaRead)
def actualizar_categoria(id: int, categoria_update: CategoriaUpdate, session: Session = get_session()):
    categoria = session.get(Categoria, id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada.")
    
    for key, value in categoria_update.dict(exclude_unset=True).items():
        setattr(categoria, key, value)
    
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria


# 🔹 Desactivar categoría
@router.delete("/{id}", status_code=200)
def desactivar_categoria(id: int, session: Session = get_session()):
    categoria = session.get(Categoria, id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada.")
    
    categoria.activo = False
    session.add(categoria)
    session.commit()
    return {"message": f"Categoría '{categoria.nombre}' desactivada correctamente."}
