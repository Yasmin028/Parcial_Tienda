from pydantic import BaseModel, Field
from typing import Optional

# CATEGORÍAS

class CategoriaBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    descripcion: Optional[str] = None
    activo: bool = True

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    descripcion: Optional[str] = None
    activo: Optional[bool] = None

class CategoriaRead(CategoriaBase):
    id: int

class Config:
    orm_mode = True


#  PRODUCTOS

class ProductoBase(BaseModel):
    nombre: str
    precio: float = Field(..., gt=0, description="El precio debe ser mayor a 0")
    stock: int = Field(..., ge=0, description="El stock no puede ser negativo") 
    disponible: bool = True
    categoria_id: Optional[int] = None

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    precio: Optional[float] = None
    stock: Optional[int] = None
    disponible: Optional[bool] = None
    categoria_id: Optional[int] = None

class ProductoRead(ProductoBase):
    id: int

class Config:
    orm_mode = True
