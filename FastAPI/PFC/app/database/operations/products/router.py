from typing import List

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select

from app.database.classes import Product, ProductCreate
from app.database.models import Product as Product_DB
from app.database.database import AsyncSession, get_db


router = APIRouter(
    prefix='/product'
)

@router.get("/{id}", response_model=Product)
async def get_spec_product(id: int, db: AsyncSession = Depends(get_db)) -> Product:
    product = await db.execute(select(Product_DB).where(Product_DB.id == id))
    result = product.scalar()
    if not result:
        raise HTTPException(status_code=404, detail=f"Product with ID {id} not found")
    return result


@router.get("", response_model=List[Product])
async def get_products(db : AsyncSession = Depends(get_db)) -> List[Product]:
    products = await db.execute(select(Product_DB))
    result = products.scalars().all()
    if not result:
        raise HTTPException(status_code=404, detail="No products found")
    return result
        
        
@router.post("/add",response_model=Product)
async def add_product(product: ProductCreate ,db: AsyncSession = Depends(get_db)) -> Product:
    new_product = Product_DB(name=product.name, description=product.description, proteins=product.proteins, fats=product.fats, carbohydrates=product.carbohydrates, calories=product.calories)
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    
    return new_product