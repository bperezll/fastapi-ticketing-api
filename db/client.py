import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from dotenv import load_dotenv

load_dotenv()  # Carga variables del archivo .env

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_SERVER = os.getenv("DB_SERVER")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Create an Engine
mariadb_url = f"mariadb+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"
engine = create_engine(mariadb_url, echo=True)

# Create session to interact with database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLAlchemy Declarative Base
class Base(DeclarativeBase):
    pass

# Session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
