from datetime import datetime
from sqlalchemy import String, Float, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

# 1. FİŞ MODELİ (Ebeveyn / Parent)
class Receipt(Base):
    __tablename__ = "receipts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    merchant_name: Mapped[str] = mapped_column(String(255), nullable=False)
    total_amount: Mapped[float] = mapped_column(Float, nullable=False)
    receipt_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # 🔗 İLİŞKİ: Bir fişin BİRDEN FAZLA (List) ürünü olabilir.
    items: Mapped[list["ReceiptItem"]] = relationship("ReceiptItem", back_populates="receipt", cascade="all, delete-orphan")


# 2. ÜRÜN KALEMİ MODELİ (Çocuk / Child)
class ReceiptItem(Base):
    __tablename__ = "receipt_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    item_name: Mapped[str] = mapped_column(String(255), nullable=False) # Örn: "Süt 1L"
    unit_price: Mapped[float] = mapped_column(Float, nullable=False)      # Örn: 35.50
    quantity: Mapped[int] = mapped_column(Integer, default=1)           # Örn: 2

    # 🪢 GÖBEK BAĞI (Foreign Key): Bu ürün HANGİ FİŞE ait?
    receipt_id: Mapped[int] = mapped_column(Integer, ForeignKey("receipts.id"), nullable=False)

    # 🔗 İLİŞKİ: Bu ürünün BİR TANE ebeveyn fişi vardır.
    receipt: Mapped["Receipt"] = relationship("Receipt", back_populates="items")