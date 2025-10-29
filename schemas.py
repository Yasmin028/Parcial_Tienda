from sqlmodel import SQLModel
from typing import Optional

# ===== Categorías =====
class CategoriaBase(SQLModel):
    nombre: str
    descripcion: Optional[str] = None

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaRead(CategoriaBase):
    id: int

# ===== Productos =====
class ProductoBase(SQLModel):
    nombre: str
    precio: float
    stock: int
    disponible: bool = True
    categoria_id: Optional[int] = None

class ProductoCreate(ProductoBase):
    pass

class ProductoRead(ProductoBase):
    id: int
