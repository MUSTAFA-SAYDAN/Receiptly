from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.core.security import create_access_token
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.services.user import UserService

router = APIRouter()


# 1. KULLANICI KAYIT ENDPOINT'İ
@router.post(
    "/register", 
    response_model=UserResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Yeni kullanıcı kaydı oluşturur"
)
def register(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):
    """Yeni müşteri kaydı alır, şifreyi hash'leyip saklar."""
    return UserService.create_user(db=db, user_in=user_in)


# 2. KULLANICI GİRİŞ ENDPOINT'İ (Token Alımı)
@router.post(
    "/login", 
    summary="Giriş yapar ve VIP Kart (JWT Access Token) üretir"
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """OAuth2 uyumlu giriş formu ile JWT token üretir."""
    user = UserService.authenticate_user(
        db=db, 
        email=form_data.username, 
        password=form_data.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-posta adresi veya şifre hatalı."
        )
    
    access_token = create_access_token(subject=user.email)
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# 3. KENDİ PROFİLİNİ GETİRME ENDPOINT'İ
@router.get(
    "/me", 
    response_model=UserResponse,
    summary="Oturum açmış kullanıcının profil detaylarını getirir"
)
def read_user_me(
    current_user: User = Depends(get_current_user)
):
    """Turnikeden geçen aktif kullanıcının bilgilerini döner."""
    return current_user