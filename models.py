from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Categoria(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, nullable=False)
    descripcion: Optional[str] = None

    productos: List["Producto"] = Relationship(back_populates="categoria")

class Producto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, nullable=False)
    precio: float
    stock: int = Field(default=0)
    disponible: bool = Field(default=True)
    categoria_id: Optional[int] = Field(default=None, foreign_key="categoria.id")

    categoria: Optional[Categoria] = Relationship(back_populates="productos")
