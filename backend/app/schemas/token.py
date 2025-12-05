from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    "schema para el token"
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    "Datos dentro del token"
    user_id : Optional[int] = None
    email: Optional[str] = None

class Login(BaseModel):
    """Schema para el login"""
    email: str
    password: str

class RefreshTokenRequest(BaseModel):
    """Schema para el refresh token"""
    refresh_token: str