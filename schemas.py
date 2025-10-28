from sqlmodel import SQLModel
from typing import Optional

class CategoriaCreate(SQLModel):
    nombre: str
    descripcion: Optional[str] = None

class CategoriaRead(SQLModel):
    id: int
    nombre: str
    descripcion: Optional[str]
    activa: bool

class ProductoCreate(SQLModel):
    nombre: str
    precio: float
    stock: int
    descripcion: Optional[str] = None
    categoria_id: int

class ProductoRead(SQLModel):
    id: int
    nombre: str
    precio: float
    stock: int
    descripcion: Optional[str]
    activo: bool
