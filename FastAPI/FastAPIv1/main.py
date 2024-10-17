from typing import Annotated

from fastapi import Depends, FastAPI, Path, Body

from sqlalchemy.orm import Session

from models import Base, User 
from database import engine, session_local
from classes import User as User_DB, UserCreate


app = FastAPI()

Base.metadata.create_all(bind=engine)

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



        
            
    