from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone

class Purchase(Base):
    __tablename__ = "purchase"
    id = Column(Integer, primary_key=True, index=True)
    Supplier_id = Column(Integer, ForeignKey("supplier.id"))
    area_id = Column(Integer, ForeignKey("area.id"), nullable=False)
    amount = Column(Float) # type: ignore
    date = Column(DateTime(timezone=True), default=lambda:datetime.now(timezone.utc))

    area = relationship("Area", back_populates="purchase")
    supplier = relationship("Supplier", back_populates="purchase")
    detail = relationship("PurchaseDetail", back_populates="purchase", cascade="all, delete-orphan")

class PurchaseDetail(Base):
    __tablename__="purchase_detail"
    id = Column(Integer, primary_key=True, index=True)
    reference = Column(String(255), unique= True)
    purchase_id = Column(Integer, ForeignKey("purchase.id"))
    product_id = Column(Integer, ForeignKey("product.id"))
    quantity = Column(Integer)
    unitaryPrice = Column("Float") # type: ignore

    product = relationship("Product", back_populate ="SaleDetail")
    purchase = relationship("PurchaseSale", back_populate ="PurchaseDetail")
