from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, NonNegativeFloat

from typing import Optional


class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Название продукта(обязательно)") 
    description: Optional[str] = Field(None, max_length=100, description="Описание продукта(не обязательно)")
    proteins: NonNegativeFloat = Field(0.0, ge=0, description="Кол-во белков(больше или равно 0)")
    fats: NonNegativeFloat = Field(0.0, ge=0, description="Кол-во жиров(больше или равно 0)")
    carbohydrates: NonNegativeFloat = Field(0.0, ge=0, description="Кол-во углеводов(больше или равно 0)")
    calories: NonNegativeFloat = Field(0.0, ge=0, le=10000, description="Кол-во калорий(больше или равно 0)")

class ProductCreate(ProductBase):
    pass
   
class Product(ProductBase):
    id: int
    
    class Config:
        from_attributes = True    
        
       
        
class UserLogin(BaseModel):
    username: str = Field(..., max_length=20, min_length = 2, description="Имя пользователя (от 3 до 50 символов)")
    password: str = Field(..., min_length=6, max_length=100, description="Пароль (минимум 8 символов)")
    
class UserCreate(UserLogin):
    email: EmailStr = Field(..., description="Email пользователя (обязательно и в формате email)")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Дата создания пользователя (автоматически заполняется)")

class User(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор пользователя, назначаемый базой данных")
    username: str = Field(...,min_length=3, max_length=50, description="Имя пользователя (от 3 до 50 символов)")
    email: EmailStr = Field(..., description="Email пользователя")
    created_at: datetime = Field(..., description="Дата создания пользователя")

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.strftime("%d.%m.%Y %H:%M")
        }

    
    
       