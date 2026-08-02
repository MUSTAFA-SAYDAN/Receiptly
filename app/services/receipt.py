from sqlalchemy.orm import Session
from app.models.receipt import Receipt
from app.schemas.receipt import ReceiptCreate, ReceiptUpdate

class ReceiptService:
    @staticmethod
    def get_all(db: Session) -> list[Receipt]:
        """Depodaki tüm fişleri kucaklayıp getiren şef metodu"""
        return db.query(Receipt).all()

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
            receipt_date=receipt_in.receipt_date
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