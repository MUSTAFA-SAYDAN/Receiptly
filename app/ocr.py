import re
import io
from PIL import Image
import pytesseract

# Windows üzerindeki Tesseract exe yolunu belirtiyoruz
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def parse_receipt_image(image_bytes: bytes) -> dict:
    """
    Gelen resim verisinden (bytes) OCR ile metin okur ve 
    mağaza adı ile toplam tutarı ayıklar.
    """
    # 1. Byte verisini Görsele (PIL Image) dönüştür
    image = Image.open(io.BytesIO(image_bytes))
    
    # 2. OCR ile Türkçe + İngilizce metin okuma
    raw_text = pytesseract.image_to_string(image, lang='tur+eng')
    
    # 3. Satır satır temizleme
    lines = [line.strip() for line in raw_text.split('\n') if line.strip()]
    
    # Varsayılan değerler
    merchant_name = "Bilinmeyen Mağaza"
    total_amount = 0.0
    
    # 4. Mağaza Adı Tespiti (Genellikle ilk dolu satırdır)
    if lines:
        merchant_name = lines[0]
        
    # 5. Toplam Tutar Tespiti (Regex ile "TOPLAM", "TOTAL" vb. yanındaki sayıları arar)
    # Örn: "TOPLAM 150.00", "TOTAL: 89,90 TL"
    amount_pattern = r'(?:TOPLAM|TOTAL|TUTAR)[^\d]*(\d+[\.,]\d{2})'
    
    match = re.search(amount_pattern, raw_text, re.IGNORECASE)
    if match:
        # Virgülü noktaya çevirip float yapıyoruz (89,90 -> 89.90)
        raw_amount = match.group(1).replace(',', '.')
        try:
            total_amount = float(raw_amount)
        except ValueError:
            total_amount = 0.0
            
    return {
        "merchant_name": merchant_name,
        "total_amount": total_amount,
        "raw_text": raw_text  # Hata ayıklama için okunan ham metni de döndürebiliriz
    }