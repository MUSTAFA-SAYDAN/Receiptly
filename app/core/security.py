from datetime import datetime, timedelta, timezone
from typing import Any, Union
import bcrypt
from jose import jwt

# Güvenlik Konfigürasyonları
SECRET_KEY = "YOUR_SUPER_SECRET_KEY_CHANGE_THIS_IN_PRODUCTION"  # Mevcut SECRET_KEY değerini koru
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_password_hash(password: str) -> str:
    """
    Şifreyi bcrypt ile hash'ler.
    Bcrypt'in 72 bayt sınırına takılmaması için girdi güvenli şekilde kesilir.
    """
    pwd_bytes = password.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Düz metin şifre ile veritabanındaki hash'lenmiş şifreyi doğrular."""
    try:
        return bcrypt.checkpw(
            plain_password.encode('utf-8')[:72],
            hashed_password.encode('utf-8')
        )
    except Exception:
        return False


def create_access_token(subject: Union[str, Any], expires_delta: timedelta | None = None) -> str:
    """JWT Access Token üretir."""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt