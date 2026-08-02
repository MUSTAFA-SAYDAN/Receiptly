from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from app.models.receipt import Receipt, ReceiptItem
from app.schemas.receipt import ReceiptCreate, ReceiptUpdate

class ReceiptService:
    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        merchant_name: str | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        min_amount: float | None = None,
        max_amount: float | None = None
    ) -> list[Receipt]:
        """Depodaki tüm fişleri filtreleyip kucaklayıp getiren şef metodu"""
        query = db.query(Receipt).options(joinedload(Receipt.items))

        # Dinamik filtreler
        if merchant_name:
            query = query.filter(Receipt.merchant_name.ilike(f"%{merchant_name}%"))
        if start_date:
            query = query.filter(Receipt.receipt_date >= start_date)
        if end_date:
            query = query.filter(Receipt.receipt_date <= end_date)
        if min_amount is not None:
            query = query.filter(Receipt.total_amount >= min_amount)
        if max_amount is not None:
            query = query.filter(Receipt.total_amount <= max_amount)

        # Sayfalama ve sıralama (En yeni fiş en üstte)
        return query.order_by(Receipt.receipt_date.desc())\
                    .offset(skip)\
                    .limit(limit)\
                    .all()

    @staticmethod
    def get_by_id(db: Session, receipt_id: int) -> Receipt | None:
        """Depodan id'ye göre spesifik fişi cımbızla çeken şef metodu"""
        return db.query(Receipt).filter(Receipt.id == receipt_id).first()

    @staticmethod
    def create(db: Session, receipt_in: ReceiptCreate) -> Receipt:
        """Yeni fiş kutusu hazırlayıp kilitli depoya koyan şef metodu"""
        db_receipt = Receipt(
            merchant_name=receipt_in.merchant_name,
            total_amount=receipt_in.total_amount,
            receipt_date=receipt_in.receipt_date,
            items=[ReceiptItem(**item.model_dump()) for item in receipt_in.items]
        )
        db.add(db_receipt)
        db.commit()
        db.refresh(db_receipt)
        return db_receipt

    @staticmethod
    def update(db: Session, db_receipt: Receipt, receipt_in: ReceiptUpdate) -> Receipt:
        """Raftaki kutunun etiketlerini güncelleyen şef metodu"""
        update_data = receipt_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_receipt, field, value)

        db.commit()
        db.refresh(db_receipt)
        return db_receipt

    @staticmethod
    def delete(db: Session, db_receipt: Receipt) -> None:
        """Raftaki kutuyu çöpe atan şef metodu"""
        db.delete(db_receipt)
        db.commit()