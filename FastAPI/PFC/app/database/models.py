from sqlalchemy import Column, Integer, String, ForeignKey, Float

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