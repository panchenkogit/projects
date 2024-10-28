from multiprocessing import get_context
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles
from sqlalchemy import select
from passlib.context import CryptContext

from app.database.classes import UserCreate, User, UserLogin
from app.database.database import AsyncSession, get_db
from app.database.models import User as UserDB

from app.database.operations.products.router import router as product_router
from app.database.database import engine, Base


app = FastAPI()
app.include_router(product_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем запросы с любых доменов
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем любые HTTP-методы
    allow_headers=["*"],  # Разрешаем любые заголовки
)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

@app.get('/', response_class=HTMLResponse)
async def main_page():
    try:
        with open("frontend/page/main_page.html", 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Page not found")
 
#хэширование пароля   
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
@app.post("/auth/register")
async def reg_user(user: UserCreate, db: AsyncSession = Depends(get_db))-> User: 
    check_user = await db.execute(select(UserDB).where(UserDB.username==user.username))
    check_email = await db.execute(select(UserDB).where(UserDB.email == user.email))
    
    if check_user.scalar() is not None:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    elif check_email.scalar() is not None:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    else:
        hashed_password = pwd_context.hash(user.password)
        
        new_user = UserDB(
            username=user.username,
            hashed_password=hashed_password,
            email=user.email
        )
        
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        
    return new_user

@app.post('/auth/login')
async def auth_user(user: UserLogin, db: AsyncSession = Depends(get_db)) -> dict:
    result = await db.execute(select(UserDB).where(UserDB.username == user.username))
    user_db = result.scalar_one_or_none()

    if user_db is None:
        raise HTTPException(status_code=404, detail="User not found or not registered")

    if not pwd_context.verify(user.password, user_db.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    return {
        "status": 200,
        "data": "Everything is fine, you are found!"
    }

