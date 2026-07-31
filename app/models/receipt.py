from datetime import datetime
from typing import Optional
from sqlalchemy import String, Float, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Receipt(Base):
    __tablename__ = "receipts"  # Veritabanındaki gerçek tablo adı

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    merchant_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    total_amount: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    receipt_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)