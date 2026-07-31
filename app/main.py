from fastapi import FastAPI
from app.api.receipts import router as receipts_router

app = FastAPI(title="Receiptly API")

# Fiş rotalarımızı uygulamaya dahil ediyoruz
app.include_router(receipts_router)

@app.get("/")
async def root():
    return {"message": "Receiptly API başarıyla çalışıyor!"}