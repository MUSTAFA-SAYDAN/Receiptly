from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# 1. Veritabanı Motoru: Fiziksel bağlantıyı kurar
engine = create_engine(settings.DATABASE_URL)

# 2. Oturum Fabrikası: İstek geldikçe veritabanı oturumu üretir
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Bağımlılık (Dependency): Her istekte oturum açar, iş bitince kapatır
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()