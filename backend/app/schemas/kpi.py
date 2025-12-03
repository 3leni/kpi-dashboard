from pydantic import BaseModel, Field, PositiveFloat
from datetime import datetime
from typing import Optional


class KPIBase(BaseModel):
    title: str
    description: Optional[str] = None
    current_value: Optional[float] = None
    target_value: Optional[float] = None
    unit: Optional[str] = None
    category: Optional[str] = None

class KPICreate(KPIBase):
    title: str = Field(..., min_length=3, max_length=255)
    current_value: PositiveFloat
    target_value: PositiveFloat

class KPIResponse(KPIBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class KPIStatsSummary(BaseModel):
    total_kpis: int
    kpis_by_category: dict
    average_compliance: float