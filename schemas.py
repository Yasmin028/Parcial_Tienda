from pydantic import BaseModel, Field
from typing import Optional

# CATEGORÍAS

from pydantic import Field, field_validator, BaseModel

class ProductoBase(BaseModel):
    nombre: str
    precio: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)

    @field_validator("precio")
    def validar_precio(cls, v):
        if v <= 0:
            raise ValueError("El precio debe ser mayor que 0")
        return v

    @field_validator("stock")
    def validar_stock(cls, v):
        if v < 0:
            raise ValueError("El stock no puede ser negativo")
        return v

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
