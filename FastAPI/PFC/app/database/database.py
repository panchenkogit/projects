from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import SQL_DB

engine = create_engine(SQL_DB,connect_args={"check_same_thread": False})

session = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()