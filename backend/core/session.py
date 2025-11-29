from sqlalchemy.orm import declarative_base,sessionmaker
from core import settings
from sqlalchemy import create_engine

Base = declarative_base()

engine= create_engine(
      settings.DATABASE_URL,
      connect_args={"sslmode": "require"},
      echo=True
   )

SessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)

def get_db():
   db= SessionLocal()
   try:
      yield db
   finally:
      db.close() 