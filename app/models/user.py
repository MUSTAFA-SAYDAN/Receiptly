from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)  # Şifreyi asla ham saklamıyoruz!
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 1 - N İlişkisi: Bir kullanıcının BİRDEN FAZLA fişi olabilir.
    receipts = relationship("Receipt", back_populates="owner", cascade="all, delete-orphan")