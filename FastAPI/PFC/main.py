from typing import List, Optional
from fastapi import Query
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.future import select

from fastapi.staticfiles import StaticFiles


from app.database.database import engine, Base, get_db, AsyncSession
from app.database.classes import Product, ProductCreate
from app.database.models import Product as Product_DB



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем запросы с любых доменов
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем любые HTTP-методы
    allow_headers=["*"],  # Разрешаем любые заголовки
)

@app.on_event("startup")
async def on_startup():
    # Создаем таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()


app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

@app.get('/', response_class=HTMLResponse)
async def main_page():
    try:
        with open("frontend/page/main_page.html", 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Page not found")

@app.get("/products/{id}", response_model=Product)
async def get__spec_product(id: int, db: AsyncSession = Depends(get_db)) -> Product:
    product = await db.execute(select(Product_DB).where(Product_DB.id == id))
    result = product.scalar()
    if not result:
        raise HTTPException(status_code=404, detail=f"Product with ID {id} not found")
    return result


@app.get("/products", response_model=List[Product])
async def get_products(db : AsyncSession = Depends(get_db)) -> List[Product]:
    products = await db.execute(select(Product_DB))
    result = products.scalars().all()
    if not result:
        raise HTTPException(status_code=404, detail="No products found")
    return result
        
        

@app.post("/product/add",response_model=Product)
async def add_product(product: ProductCreate ,db: AsyncSession = Depends(get_db)) -> Product:
    new_product = Product_DB(name=product.name, description=product.description, proteins=product.proteins, fats=product.fats, carbohydrates=product.carbohydrates, calories=product.calories)
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    
    return new_product

    

