from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DepartamentBase(BaseModel):
    name: str
    description: Optional[str] = None
    
class DepartamentCreate(DepartamentBase):
    pass 

class DepartamentResponse(DepartamentBase):
    id: int
    created_at:datetime

    class Config:
        from_attributes = True