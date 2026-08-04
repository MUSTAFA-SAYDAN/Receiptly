from fastapi import FastAPI
from app.api.receipts import router as receipts_router
from app.api.auth import router as auth_router  # 🔑 Auth rotamızı içe aktarıyoruz
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Receiptly API")

# Frontend'in Backend ile konuşmasına izin veren CORS ayarı
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Geliştirme aşamasında tüm kökenlere izin veriyoruz
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth ve Fiş rotalarımızı uygulamaya dahil ediyoruz
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(receipts_router)

@app.get("/")
async def root():
    return {"message": "Receiptly API başarıyla çalışıyor!"}