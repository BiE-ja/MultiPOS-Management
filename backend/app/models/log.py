# to memorise user's action in the app
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.database import Base
from datetime import datetime, timezone
from sqlalchemy.orm import relationship

class Log(Base):
    __tablename__ = "log"
    id = Column(Integer, primary_key=True, index=True)
    dateAction = date = Column(DateTime(timezone=True), default=lambda:datetime.now(timezone.utc))
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    area_id = Column(Integer, ForeignKey("area.id"), nullable=False)
    action = Column(String)

    user = relationship("User", back_populates="Log")