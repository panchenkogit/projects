from typing import Annotated

from fastapi import Depends, FastAPI, Path, Body
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from models import Base, User 
from database import engine, session_local
from classes import User as User_DB, UserCreate


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем запросы с любых доменов
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем любые HTTP-методы
    allow_headers=["*"],  # Разрешаем любые заголовки
)

async def create_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
     
@app.post("/users/add", response_model=User_DB)
async def add_user(user: UserCreate,db: Session = Depends(create_db)) -> User:
    new_user = User(name=user.name, email=user.email, age=user.age)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@app.get("/users/all")
async def get_user(db: Session = Depends(create_db) ):
    all_users = db.query(User.all())
    return all_users

@app.get("/users/search")
async def get_user_for_name(name: str,db: Session = Depends(create_db) ):
    users = db.query(User).filter(User.name == name).all()
    if users:
        return users
    else:
        return {
            "status" : 404,
            "detail" : "User not found"
        }

        
            
    