# models.py
from sqlmodel import SQLModel, Field
from typing import Optional

class Producto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    precio: float
    categoria_id: Optional[int] = Field(default=None, foreign_key="categoria.id")

class Categoria(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
