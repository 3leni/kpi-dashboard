from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.database.database import get_db
from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.schemas.token import Token, RefreshTokenRequest
from app.schemas.user import UserCreate
from app.services.user_service import UserService
from app.services.demo_service import clean_demo_data, seed_demo_data
from app.api.v1.deps import get_current_user

router = APIRouter()
login_attemps = {}
@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login del usuario"""
    user = UserService.authenticate_user(db, email=form_data.username, password=form_data.password)
    email = form_data.username
    now = datetime.now()
    attemps = login_attemps.get(email, []) 
    attemps = [t for t in attemps if now - t < timedelta(minutes=1)]
    if len(attemps) >= 5:
        raise HTTPException(
            status_code=status.HTTP_429,
            detail="Too many login attempts. Try again later.",
        )
    if not user:
        attemps.append(now)
        login_attemps[email] = attemps
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    login_attemps[email] = []
    access_token = create_access_token(data={"user_id": user.id, "email": user.email})
    refresh_token = create_refresh_token(data={"user_id": user.id, "email": user.email})

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/register", response_model=Token)
def register( user_data: UserCreate, db: Session = Depends(get_db)):
    """Registrar nuevo usuario"""
    existing_user =  UserService.get_user_by_email(db, email=user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    user = UserService.create_user(db, user_data)
    access_token = create_access_token(data={"user_id": user.id, "email": user.email})
    refresh_token = create_refresh_token(data={"user_id": user.id, "email": user.email})

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/refresh", response_model=Token)
def refresh(token_data: RefreshTokenRequest, db: Session = Depends(get_db)):
    """Obtener un nuevo access token usando el refresh token"""
    payload = verify_token(token_data.refresh_token)

    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    
    user_id = payload.get("user_id")
    user = UserService.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    
    access_token = create_access_token(data={"user_id": user.id, "email": user.email})
    new_refresh_token = create_refresh_token(data={"user_id": user.id, "email": user.email})

    return {"access_token": access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}

@router.post("/me")
def get_current_user_info(current_user = Depends(get_current_user)):
    """Obtener información del usuario actual"""
    return {
        "id" : current_user.id,
        "email" : current_user.email,
        "full_name" : current_user.full_name,
        "is_active" : current_user.is_active
    }

@router.post("logout")
def logout(current_user = Depends(get_current_user)):
    """Cerrar sesión del usuario"""
    return {"message": f"User {current_user} has logged out successfully"}

@router.post("/demo-login", response_model=Token)
def demo_login(db: Session = Depends(get_db)):
    """Demo login de usuario"""
    email="demo@demo.com" 
    password="demo"
    full_name="Demo User"
    user = UserService.get_user_by_email(db, email)
    if not user:
        user_data = UserCreate(email=email, password=password, full_name=full_name)
        user = UserService.create_user(db, user_data)
    
    access_token = create_access_token(data={"user_id": user.id, "email": user.email}, expires_delta=timedelta(hours=1))
    refresh_token = create_refresh_token(data={"user_id": user.id, "email": user.email})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/demo-login2", response_model=Token)
def demo_login(db: Session = Depends(get_db)):
    """Demo login de usuario"""
    email="demo@demo.com" 
    password="demo"
    full_name="Demo User"
    user = UserService.get_user_by_email(db, email)
    if not user:
        user_data = UserCreate(email=email, password=password, full_name=full_name, is_demo_user=True)
        user = UserService.create_user(db, user_data)

    if user.is_demo_user == False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid demo user",
        )
    clean_demo_data(db, user)
    seed_demo_data(db, user)
    access_token = create_access_token(data={"user_id": user.id, "email": user.email}, expires_delta=timedelta(hours=1))
    refresh_token = create_refresh_token(data={"user_id": user.id, "email": user.email})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}