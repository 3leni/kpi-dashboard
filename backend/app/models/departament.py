from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.database import Base

class Departaments(Base):
    __tablename__ = "departaments" 

    id = Column(Integer, primary_key=True, index=True )
    name = Column(String(255), nullable=False )
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
