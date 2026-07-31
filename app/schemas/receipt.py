from datetime import datetime
from pydantic import BaseModel

# Ortak alanlar
class ReceiptBase(BaseModel):
    merchant_name: str
    total_amount: float
    receipt_date: datetime

# Fiş eklerken (POST) kullanıcıdan istenecek veriler
class ReceiptCreate(ReceiptBase):
    pass

# Fişi ekrana basarken (Response) döneceğimiz veri formatı
class ReceiptResponse(ReceiptBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # SQLAlchemy modelleriyle Pydantic'i uyumlu çalıştırır