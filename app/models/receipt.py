from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import String, Float, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

# IDE ve Type Checker döngüsel import hatası vermesin diye sadece tip kontrolünde import ediyoruz
if TYPE_CHECKING:
    from app.models.user import User


# 1. FİŞ MODELİ (Ebeveyn / Parent)
class Receipt(Base):
    __tablename__ = "receipts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    merchant_name: Mapped[str] = mapped_column(String(255), nullable=False)
    total_amount: Mapped[float] = mapped_column(Float, nullable=False)
    receipt_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # 🪢 GÖBEK BAĞI (Foreign Key): Bu fiş HANGİ KULLANICIYA ait?
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)

    # 🔗 İLİŞKİLER
    # A) Fişin Sahibi (Tek bir Kullanıcı)
    owner: Mapped["User"] = relationship("User", back_populates="receipts")

    # B) Fişin Ürünleri (Birden fazla Ürün)
    items: Mapped[list["ReceiptItem"]] = relationship(
        "ReceiptItem", back_populates="receipt", cascade="all, delete-orphan"
    )


# 2. ÜRÜN KALEMİ MODELİ (Çocuk / Child)
class ReceiptItem(Base):
    __tablename__ = "receipt_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    item_name: Mapped[str] = mapped_column(String(255), nullable=False)  # Örn: "Süt 1L"
    unit_price: Mapped[float] = mapped_column(Float, nullable=False)      # Örn: 35.50
    quantity: Mapped[int] = mapped_column(Integer, default=1)           # Örn: 2

    # 🪢 GÖBEK BAĞI (Foreign Key): Bu ürün HANGİ FİŞE ait?
    receipt_id: Mapped[int] = mapped_column(Integer, ForeignKey("receipts.id"), nullable=False)

    # 🔗 İLİŞKİ: Bu ürünün BİR TANE ebeveyn fişi vardır.
    receipt: Mapped["Receipt"] = relationship("Receipt", back_populates="items")