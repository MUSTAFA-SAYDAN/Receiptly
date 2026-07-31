from fastapi import FastAPI

app = FastAPI(title="Receiptly")

@app.get("/")
async def root():
    return {"message": "Receiptly API başarıyla çalışıyor!"}