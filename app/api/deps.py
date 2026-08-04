from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import SECRET_KEY, ALGORITHM
from app.db.session import AsyncSessionLocal
from app.models.user import User
from app.services.user import UserService

# OAuth2 şeması: Swagger UI ve FastAPI için token alışveriş noktasını belirler
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# 1. VERİTABANI OTURUM BAĞIMLILIĞI (DB Session Injector)
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Her istek için bir veritabanı oturumu açar, işlem bitince otomatik kapatır."""
    async with AsyncSessionLocal() as session:
        yield session


# 2. AKTİF KULLANICI KONTROLÜ (VIP Kart & Kimlik Doğrulama Turnikesi)
async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """
    İstekteki JWT Token'ı çözer, içindeki e-posta bilgisini doğrular
    ve veritabanından aktif kullanıcıyı çekip döndürür.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Kimlik doğrulaması başarısız. Geçersiz token veya oturum süresi dolmuş.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # 1. VIP Kartı (JWT Token) gizli anahtarımızla çözüyoruz
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except (JWTError, ValidationError):
        raise credentials_exception

    # 2. E-posta ile veritabanından kullanıcıyı çekiyoruz
    user = await UserService.get_by_email(db, email=email)
    if user is None:
        raise credentials_exception

    # 3. Kullanıcı hesabı dondurulmuş veya pasif mi?
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Kullanıcı hesabı pasif durumda."
        )

    return user