from __future__ import annotations

from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Log(Base):
    __tablename__ = "log"
    id = Column(Integer, primary_key=True, index=True)
    dateAction = Column(DateTime(timezone=True), default=lambda:datetime.now(timezone.utc))
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    area_id = Column(Integer, ForeignKey("area.id"), nullable=False)
    action = Column(String)

    user = relationship("User", back_populates="log")
    area = relationship("Area", back_populates="log")