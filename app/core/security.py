from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from passlib.context import CryptContext

# 🔐 GÜVENLİK AYARLARI
# Gerçek canlıya çıkarken bu SECRET_KEY'i .env dosyasında saklayacağız.
SECRET_KEY = "SUPER_SECRET_GIZLI_ANAHTAR_BURAYA_GELECEK_KIMSENIN_BILMEMESI_LAZIM"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # Token 24 saat geçerli olsun (1 gün)

# Passlib Şifreleme Motoru (Bcrypt algoritması kullanıyoruz)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 1. ŞİFRE İŞLEMLERİ (PASSWORD HASHING)

def get_password_hash(password: str) -> str:
    """Ham şifreyi (ör: '123456') alır ve geri döndürülemez bir bcrypt hash'ine çevirir."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Kullanıcının girdiği ham şifre ile veritabanındaki hash'i karşılaştırır."""
    return pwd_context.verify(plain_password, hashed_password)


# 2. JWT TOKEN (GİRİŞ KART) İŞLEMLERİ

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Başarıyla giriş yapan kullanıcıya imzalı bir JWT Token (VIP Kartı) üretir.
    """
    to_encode = data.copy()
    
    # Token'ın son kullanma tarihini hesapla
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Token icine "exp" (expiration / bitiş tarihi) bilgisini gömüyoruz
    to_encode.update({"exp": expire})
    
    # Gizli anahtarımızla damgalayıp token'ı şifreliyoruz
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt