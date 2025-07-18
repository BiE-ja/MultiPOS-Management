from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone

class Sale(Base):
    __tablename__ = "sale"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customer.id"))
    area_id = Column(Integer, ForeignKey("area.id"), nullable=False)
    reference = Column(String(255), unique= True)
    amount = Column(Float, nullable=True) # type: ignore
    date = Column(DateTime(timezone=True), default=lambda:datetime.now(timezone.utc))

    area = relationship("Area", back_populates="sale")
    customer = relationship("Customer", back_populate ="Sale")
    detail = relationship("SaleDetail", back_populates="Sale", cascade="all, delete-orphan")

class SaleDetail(Base):
    __tablename__="sale_detail"
    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sale.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"))
    quantity = Column(Integer)
    unitaryPrice = Column("Float") # type: ignore

    product = relationship("Product", back_populate ="SaleDetail")
    Sale = relationship("Sale", back_populate ="SaleDetail")