# app/services/analytics.py
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.receipt import Receipt

class AnalyticsService:
    @staticmethod
    def get_summary(db: Session) -> dict:
        # 1. Toplam Harcama ve Toplam Fiş Sayısı
        total_stats = db.query(
            func.coalesce(func.sum(Receipt.total_amount), 0).label("total_spent"),
            func.count(Receipt.id).label("total_receipts")
        ).first()

        # 2. En Çok Harcama Yapılan İlk 5 Mağaza (Group By & Order By)
        top_merchants_raw = db.query(
            Receipt.merchant_name,
            func.sum(Receipt.total_amount).label("total_spent"),
            func.count(Receipt.id).label("receipt_count")
        ).group_by(Receipt.merchant_name)\
         .order_by(func.sum(Receipt.total_amount).desc())\
         .limit(5)\
         .all()

        top_merchants = [
            {
                "merchant_name": row.merchant_name,
                "total_spent": float(row.total_spent),
                "receipt_count": row.receipt_count
            }
            for row in top_merchants_raw
        ]

        return {
            "total_spent": float(total_stats.total_spent),
            "total_receipts": total_stats.total_receipts,
            "top_merchants": top_merchants
        }