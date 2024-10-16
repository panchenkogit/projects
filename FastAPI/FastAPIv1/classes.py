from pydantic import BaseModel


    
class User(BaseModel):
    id: int
    name: str
    email: str
    age: int
    
    class Config:
        from_attributes = True
        
class UserCreate(User):
    pass