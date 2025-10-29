from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, Session
from db import get_session
from models import Categoria
from schemas import CategoriaCreate, CategoriaRead

router = APIRouter()

# Crear categoría
@router.post("/", response_model=CategoriaRead, status_code=201)
def crear_categoria(categoria: CategoriaCreate, session: Session = Depends(get_session)):
    db_categoria = session.exec(select(Categoria).where(Categoria.nombre == categoria.nombre)).first()
    if db_categoria:
        raise HTTPException(status_code=409, detail="La categoría ya existe.")
    
    nueva_categoria = Categoria.from_orm(categoria)
    session.add(nueva_categoria)
    session.commit()
    session.refresh(nueva_categoria)
    return nueva_categoria

# Listar todas
@router.get("/", response_model=list[CategoriaRead])
def listar_categorias(session: Session = Depends(get_session)):
    categorias = session.exec(select(Categoria)).all()
    return categorias

# Obtener una por ID
@router.get("/{categoria_id}", response_model=CategoriaRead)
def obtener_categoria(categoria_id: int, session: Session = Depends(get_session)):
    categoria = session.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada.")
    return categoria

# Eliminar
@router.delete("/{categoria_id}", status_code=200)
def eliminar_categoria(categoria_id: int, session: Session = Depends(get_session)):
    categoria = session.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada.")
    session.delete(categoria)
    session.commit()
    return {"message": "Categoría eliminada correctamente."}

# Consulta relacional: obtener categoría con productos
@router.get("/{categoria_id}/productos")
def obtener_categoria_con_productos(categoria_id: int, session: Session = Depends(get_session)):
    """
    Devuelve una categoría junto con todos sus productos asociados.
    """
    categoria = session.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return {
        "categoria": categoria.nombre,
        "descripcion": categoria.descripcion,
        "productos": categoria.productos
    }
