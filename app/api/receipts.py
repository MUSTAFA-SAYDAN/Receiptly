from typing import List
from fastapi import APIRouter, Depends, status
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