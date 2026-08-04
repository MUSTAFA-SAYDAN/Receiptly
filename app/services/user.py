from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password


class UserService:
    
    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        """E-posta adresine göre veritabanında kullanıcı arar (Senkron)."""
        return db.scalars(select(User).where(User.email == email)).first()

    @staticmethod
    def create_user(db: Session, user_in: UserCreate) -> User:
        """
        Yeni bir kullanıcı kaydeder.
        E-posta zaten varsa hata fırlatır, şifreyi hash'leyerek saklar.
        """
        # 1. Aynı e-posta adresiyle daha önce kayıt olunmuş mu?
        existing_user = UserService.get_by_email(db, email=user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bu e-posta adresi zaten kullanımda."
            )
        
        # 2. Şifreyi güvenli hale getir (Hash'le)
        hashed_pwd = get_password_hash(user_in.password)
        
        # 3. Yeni kullanıcıyı oluştur ve veritabanına yaz
        db_user = User(
            email=user_in.email,
            hashed_password=hashed_pwd
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """
        Kullanıcı girişini doğrular.
        E-posta veya şifre yanlışsa None döner.
        """
        user = UserService.get_by_email(db, email=email)
        if not user:
            return None
        
        # Girdiği ham şifre ile veritabanındaki hash eşleşiyor mu?
        if not verify_password(password, user.hashed_password):
            return None
            
        return user