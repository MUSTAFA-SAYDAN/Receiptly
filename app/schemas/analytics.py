from pydantic import BaseModel

class MerchantSummary(BaseModel):
    merchant_name: str
    total_spent: float
    receipt_count: int

class AnalyticsSummaryResponse(BaseModel):
    total_spent: float
    total_receipts: int
    top_merchants: list[MerchantSummary]