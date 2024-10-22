from pydantic import BaseModel, Field, NonNegativeFloat
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
       