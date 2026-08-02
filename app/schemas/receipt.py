from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

# 1. ÜRÜN KALEMİ (RECEIPT ITEM) ŞEMALARI
class ReceiptItemBase(BaseModel):
    item_name: str = Field(..., min_length=1, max_length=255)
    unit_price: float = Field(..., gt=0)
    quantity: int = Field(default=1, gt=0)

class ReceiptItemCreate(ReceiptItemBase):
    pass

class ReceiptItemResponse(ReceiptItemBase):
    id: int
    receipt_id: int

    model_config = ConfigDict(from_attributes=True)


# 2. FİŞ (RECEIPT) ŞEMALARI
class ReceiptBase(BaseModel):
    merchant_name: str = Field(..., min_length=1, max_length=255)
    total_amount: float
    receipt_date: datetime | None = None

class ReceiptCreate(ReceiptBase):
    # 🔗 Fiş eklerken ürün listesini de kabul ediyoruz!
    items: list[ReceiptItemCreate] = []

class ReceiptResponse(ReceiptBase):
    id: int
    created_at: datetime
    items: list[ReceiptItemResponse] = []

    model_config = ConfigDict(from_attributes=True)

class ReceiptUpdate(BaseModel):
    merchant_name: str | None = Field(default=None, min_length=1, max_length=255)
    total_amount: float | None = Field(default=None, gt=0)
    receipt_date: datetime | None = None