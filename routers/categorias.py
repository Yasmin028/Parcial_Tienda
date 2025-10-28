from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select, Session
from db import get_session
from models import Categoria
from schemas import CategoriaCreate, CategoriaRead

router = APIRouter(prefix="/categorias", tags=["Categorias"])

@router.post("/", response_model=CategoriaRead)
def crear_categoria(data: CategoriaCreate, session: Session = Depends(get_session)):
    existe = session.exec(select(Categoria).where(Categoria.nombre == data.nombre)).first()
    if existe:
        raise HTTPException(status_code=409, detail="Nombre de categoría ya existe")
    nueva = Categoria(nombre=data.nombre, descripcion=data.descripcion)
    session.add(nueva)
    session.commit()
    session.refresh(nueva)
    return nueva

@router.get("/", response_model=list[CategoriaRead])
def listar_categorias(session: Session = Depends(get_session)):
    return session.exec(select(Categoria).where(Categoria.activa == True)).all()
