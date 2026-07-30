from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

# 1. Ana Su Borusu (Engine): Veritabanı ile fiziksel bağlantıyı kurar
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,  # Geliştirme aşamasında çalıştırılan SQL sorgularını terminalde gösterir
    future=True,
)

# 2. Vana Fabrikası (Session Local): İstek geldikçe veritabanı oturumu üretir
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


# 3. Garsona Mutfak Musluğu Veren Fonksiyon (Dependency)
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()