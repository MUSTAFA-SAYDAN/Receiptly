from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.receipt import ReceiptCreate, ReceiptResponse, ReceiptUpdate
from app.services.receipt import ReceiptService

router = APIRouter(prefix="/receipts", tags=["Receipts"])

# 1. YENİ FİŞ EKLEME (POST)
@router.post("/", response_model=ReceiptResponse, status_code=status.HTTP_201_CREATED)
def create_receipt(receipt_in: ReceiptCreate, db: Session = Depends(get_db)):
    return ReceiptService.create(db=db, receipt_in=receipt_in)

# 2. TÜM FİŞLERİ LİSTELEME (GET)
@router.get("/", response_model=List[ReceiptResponse])
def list_receipts(db: Session = Depends(get_db)):
    return ReceiptService.get_all(db=db)

# 3. SPESİFİK FİŞİ GETİRME (GET /{receipt_id})
@router.get("/{receipt_id}", response_model=ReceiptResponse)
def get_receipt(receipt_id: int, db: Session = Depends(get_db)):
    db_receipt = ReceiptService.get_by_id(db=db, receipt_id=receipt_id)
    if not db_receipt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Aradığınız fiş depoda bulunamadı!"
        )
    return db_receipt

# 4. FİŞ GÜNCELLEME (PUT /{receipt_id})
@router.put("/{receipt_id}", response_model=ReceiptResponse)
def update_receipt(receipt_id: int, receipt_in: ReceiptUpdate, db: Session = Depends(get_db)):
    db_receipt = ReceiptService.get_by_id(db=db, receipt_id=receipt_id)
    if not db_receipt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Güncellenecek fiş bulunamadı!"
        )
    return ReceiptService.update(db=db, db_receipt=db_receipt, receipt_in=receipt_in)

# 5. FİŞ SİLME (DELETE /{receipt_id})
@router.delete("/{receipt_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_receipt(receipt_id: int, db: Session = Depends(get_db)):
    db_receipt = ReceiptService.get_by_id(db=db, receipt_id=receipt_id)
    if not db_receipt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Silinecek fiş depoda bulunamadı!"
        )
    ReceiptService.delete(db=db, db_receipt=db_receipt)
    return None