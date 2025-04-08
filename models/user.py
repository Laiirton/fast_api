from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """Modelo base para usuários"""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None

class UserCreate(UserBase):
    """Modelo para criação de usuários"""
    email: EmailStr
    username: str
    password: str
    full_name: str
    cpf: str
    birth_date: Optional[str] = None

class UserLogin(BaseModel):
    """Modelo para login de usuários"""
    username: str
    password: str

class UserResponse(BaseModel):
    """Modelo para resposta de usuários"""
    id: int
    username: Optional[str] = None
    email: EmailStr
    full_name: str
    cpf: Optional[str] = None
    birth_date: Optional[str] = None
    status: Optional[str] = None
    role: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    """Modelo para token de acesso"""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Modelo para dados do token"""
    username: Optional[str] = None
    user_id: Optional[int] = None
