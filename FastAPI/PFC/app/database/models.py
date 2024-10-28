from sqlalchemy.sql import func
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Float

from app.database.database import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    proteins = Column(Float)
    fats = Column(Float)
    carbohydrates = Column(Float)
    calories = Column(Float)
    

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, unique=True)
    hashed_password = Column(String,nullable=False)
    email = Column(String, index=True, unique=True)
    created_at = Column(DateTime, default=func.now())
