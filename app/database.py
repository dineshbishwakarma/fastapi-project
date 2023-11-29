from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# SQLALCHEMY_DB_URL = 'postgresql://<username>:<password>@<ip-address>/hostname>/<db-name>'
SQLALCHEMY_DB_URL = f'postgresql://{settings.database_hostname}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()