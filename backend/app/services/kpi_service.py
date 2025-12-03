# backend/app/services/kpi_service.py
from sqlalchemy.orm import Session
from app.models.kpi import KPI
from app.schemas.kpi import KPICreate

class KPIService:
    @staticmethod
    def get_kpis(db: Session, skip: int = 0, limit: int = 100):
        return db.query(KPI).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_kpi_by_id(db: Session, kpi_id: int):
        return db.query(KPI).filter(KPI.id == kpi_id).first()
    
    @staticmethod
    def create_kpi(db: Session, kpi: KPICreate, user_id: int):
        db_kpi = KPI(
            title=kpi.title,
            description=kpi.description,
            current_value=kpi.current_value,
            target_value=kpi.target_value,
            unit=kpi.unit,
            category=kpi.category,
            created_by=user_id
        )
        db.add(db_kpi)
        db.commit()
        db.refresh(db_kpi)
        return db_kpi
    
    @staticmethod
    def update_kpi(db: Session, kpi_id: int, kpi_update: KPICreate):
        db_kpi = db.query(KPI).filter(KPI.id == kpi_id).first()
        if db_kpi:
            for field, value in kpi_update.dict(exclude_unset=True).items():
                setattr(db_kpi, field, value)
            db.commit()
            db.refresh(db_kpi)
        return db_kpi
    
    @staticmethod
    def delete_kpi(db: Session, kpi_id: int):
        db_kpi = db.query(KPI).filter(KPI.id == kpi_id).first()
        if db_kpi:
            db.delete(db_kpi)
            db.commit()
            return True
        return False
    
    @staticmethod
    def get_kpis_by_category(db: Session, category: str):
        return db.query(KPI).filter(KPI.category == category).all()