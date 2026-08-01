from typing import List
from fastapi import APIRouter, Depends, status ,HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.receipt import Receipt
from app.schemas.receipt import ReceiptCreate, ReceiptResponse

router = APIRouter(prefix="/receipts", tags=["Receipts"])

# 1. YENİ FİŞ EKLEME (POST)
@router.post("/", response_model=ReceiptResponse, status_code=status.HTTP_201_CREATED)
def create_receipt(receipt_in: ReceiptCreate, db: Session = Depends(get_db)):
    db_receipt = Receipt(
        merchant_name=receipt_in.merchant_name,
        total_amount=receipt_in.total_amount,
        receipt_date=receipt_in.receipt_date
    )
    db.add(db_receipt)
    db.commit()
    db.refresh(db_receipt)
    return db_receipt

# 2. TÜM FİŞLERİ LİSTELEME (GET)
@router.get("/", response_model=List[ReceiptResponse])
def list_receipts(db: Session = Depends(get_db)):
    return db.query(Receipt).all()

# 3. SPESİFİK FİŞİ GETİRME (GET /{receipt_id})
@router.get("/{receipt_id}", response_model=ReceiptResponse)
def get_receipt(receipt_id: int, db: Session = Depends(get_db)):
    db_receipt = db.query(Receipt).filter(Receipt.id == receipt_id).first()
    if not db_receipt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Aradığınız fiş depoda bulunamadı!"
        )
    return db_receipt

# 4. FİŞ SİLME (DELETE /{receipt_id})
@router.delete("/{receipt_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_receipt(receipt_id: int, db: Session = Depends(get_db)):
    db_receipt = db.query(Receipt).filter(Receipt.id == receipt_id).first()
    if not db_receipt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Silmek istediğiniz fiş zaten depoda yok!"
        )
    db.delete(db_receipt)
    db.commit()
    return None