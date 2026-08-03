from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict

# 1. ORTAK ŞABLON (Base Schema)
# Tüm kullanıcı şemalarında ortak olan alanlar
class UserBase(BaseModel):
    email: EmailStr  # Pydantic otomatik olarak e-posta formatında olup olmadığını denetler (ör: test@mail.com)


# 2. KAYIT FORMU (User Create Request)
# Müşteri kayıt olurken bize e-posta VE şifre gönderecek
class UserCreate(UserBase):
    password: str


# 3. YANIT FORMU (User Response)
# Dış dünyaya yanıt dönerken KESİNLİKLE 'password' veya 'hashed_password' DÖNMÜYORUZ!
class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    # SQLAlchemy model nesnelerini Pydantic şemasına otomatik çevirebilmesi için (Pydantic v2 stili):
    model_config = ConfigDict(from_attributes=True)