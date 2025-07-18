from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Supplier(Base):
    __tablename__= "supplier"
    id = Column(Integer, primary_key=True, index=True)
    name=Column(String)
    email= Column(String, unique = True, index = True)
    area_id = Column(Integer, ForeignKey("area.id"), nullable=False)

    area = relationship("Area", back_populates="supplier")
    product = relationship("Product", back_populates="supplier")
    purchase = relationship("Purchase", back_populates="supplier")