from fastapi import FastAPI
from app.api.receipts import router as receipts_router
from app.api.auth import router as auth_router  # 🔑 Auth rotamızı içe aktarıyoruz

app = FastAPI(title="Receiptly API")

# Auth ve Fiş rotalarımızı uygulamaya dahil ediyoruz
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(receipts_router)

@app.get("/")
async def root():
    return {"message": "Receiptly API başarıyla çalışıyor!"}