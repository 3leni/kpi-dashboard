# backend/app/core/config.py - ACTUALIZADO
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "KPI Dashboard"
    PROJECT_VERSION: str = "1.0.0"
    
    # Usar SQLite para desarrollo (más fácil)
    DATABASE_URL: str = "sqlite:///./kpi_dashboard.db"
    
settings = Settings()