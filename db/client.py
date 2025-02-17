from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Create an Engine
mariadb_url = f"mariadb+pymysql://{"root"}:{"o`?ZfVT?p|aK+]!O"}@{"localhost"}:{3306}/{"fastapi_test_01"}"
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