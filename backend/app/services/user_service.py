# backend/app/services/user_service.py
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from passlib.context import CryptContext

# Configuración para hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def create_user(db: Session, user: UserCreate):
        hashed_password = UserService.get_password_hash(user.password)
        db_user = User(
            email=user.email,
            hashed_password=hashed_password,
            full_name=user.full_name
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod 
    def update_user(db: Session, user_id: int, user: UserUpdate):
        db_user = UserService.get_user_by_id(db, user_id)
        if not db_user:
            return None
        if user.email:
            db_user.email = user.email
        if user.full_name:
            db_user.full_name = user.full_name
        if user.password:
            db_user.hashed_password = UserService.get_password_hash(user.password)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def delete_user(db: Session, user_id: int):
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            return None
        db.delete(user)
        db.commit()
        return user
    
    @staticmethod
    def update_active_user(db: Session, user_id: int, is_active: bool):
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            return None
        user.is_active = is_active
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100):
        return db.query(User).offset(skip).limit(limit).all()