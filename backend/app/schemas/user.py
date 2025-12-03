from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
# Esquema base
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    is_active: Optional[bool] = True

# Esquema para crear usuario
class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    password: Optional[str] = None

# Esquema para respuesta (lo que devolvemos al frontend)
class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Reemplaza orm_mode en Pydantic v2