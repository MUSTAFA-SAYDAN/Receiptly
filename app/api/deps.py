from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.security import SECRET_KEY, ALGORITHM
from app.db.session import get_db  # Mevcut get_db fonksiyonunu kullanıyoruz
from app.models.user import User
from app.services.user import UserService

# Token alışveriş noktasını main.py'deki prefix="/auth" yapısına uyarlıyoruz
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    db: Session = Depends(get_db),
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
        # 1. JWT Token'ı çözüyoruz
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except (JWTError, ValidationError):
        raise credentials_exception

    # 2. E-posta ile veritabanından kullanıcıyı çekiyoruz (Senkron çağrı)
    user = UserService.get_by_email(db, email=email)
    if user is None:
        raise credentials_exception

    # 3. Kullanıcı pasif mi kontrolü
    if hasattr(user, "is_active") and not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Kullanıcı hesabı pasif durumda."
        )

    return user