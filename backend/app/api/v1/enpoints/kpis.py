# backend/app/api/v1/endpoints/kpis.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.schemas.kpi import KPIResponse, KPICreate
from app.services.kpi_service import KPIService

router = APIRouter()

# GET /api/v1/kpis - Obtener todos los KPIs
@router.get("/", response_model=List[KPIResponse])
def get_kpis(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtener todos los KPIs con paginación
    """
    kpis = KPIService.get_kpis(db, skip=skip, limit=limit)
    return kpis

# GET /api/v1/kpis/{kpi_id} - Obtener un KPI por ID
@router.get("/{kpi_id}", response_model=KPIResponse)
def get_kpi(kpi_id: int, db: Session = Depends(get_db)):
    """
    Obtener un KPI específico por su ID
    """
    kpi = KPIService.get_kpi_by_id(db, kpi_id)
    if kpi is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="KPI no encontrado"
        )
    return kpi

# POST /api/v1/kpis - Crear nuevo KPI
@router.post("/", response_model=KPIResponse)
def create_kpi(kpi: KPICreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo KPI
    """
    # Por ahora usamos user_id 1 como demo - luego implementaremos autenticación
    return KPIService.create_kpi(db, kpi, user_id=1)

# PUT /api/v1/kpis/{kpi_id} - Actualizar KPI
@router.put("/{kpi_id}", response_model=KPIResponse)
def update_kpi(kpi_id: int, kpi_update: KPICreate, db: Session = Depends(get_db)):
    """
    Actualizar un KPI existente
    """
    kpi = KPIService.update_kpi(db, kpi_id, kpi_update)
    if kpi is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="KPI no encontrado"
        )
    return kpi

# DELETE /api/v1/kpis/{kpi_id} - Eliminar KPI
@router.delete("/{kpi_id}")
def delete_kpi(kpi_id: int, db: Session = Depends(get_db)):
    """
    Eliminar un KPI
    """
    success = KPIService.delete_kpi(db, kpi_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="KPI no encontrado"
        )
    return {"message": "KPI eliminado correctamente"}

# GET /api/v1/kpis/category/{category} - Obtener KPIs por categoría
@router.get("/category/{category}", response_model=List[KPIResponse])
def get_kpis_by_category(category: str, db: Session = Depends(get_db)):
    """
    Obtener KPIs por categoría
    """
    kpis = KPIService.get_kpis_by_category(db, category)
    return kpis

@router.get("/stats/summary") 
def get_kpi_summary( db:Session = Depends(get_db)):
    """
    Obtener resumen de KPIs
    """
    kpis = KPIService.get_kpis(db,skip=0,limit=100)
    total_kpis = len(kpis) #len()

    kpis_by_category= {}
    for kpi in kpis:
        category = kpi.category
        kpis_by_category[category] = kpis_by_category.get(category,0) + 1

    if total_kpis > 0:
        average_compliance = sum(k.current_value / k.target_value for k in kpis)/ total_kpis
    else:
        average_compliance = 0
    return {
        "total_kpis": total_kpis,
        "kpis_by_category": kpis_by_category,
        "average_compliance": average_compliance
    }
