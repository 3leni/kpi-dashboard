# backend/app/core/config.py - ACTUALIZADO
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "KPI Dashboard"
    PROJECT_VERSION: str = "1.0.0"
    
    # Usar SQLite para desarrollo (más fácil)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./kpi_dashboard.db")

    #JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "JKL09IL7")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    
    
settings = Settings()