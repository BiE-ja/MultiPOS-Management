
# Represente un point de vente
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from backend.app.database import Base

# Represente a point of sale
class Area (Base):
    __tablename__="area"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    location = Column(String(255))
    owner = Column(Integer, ForeignKey("user.id"), nullable=False)

    user = relationship("User", back_populates="area")
    employee = relationship("Employee", back_populates="area", cascade = "all, delete-orphan")
    customer = relationship("Customer", back_populates="area", cascade = "all, delete-orphan")
    product = relationship("Product", back_populates="area", cascade = "all, delete-orphan")
    purchase = relationship("Purchase", back_populates="area", cascade="all, delete-orphan")
    sale = relationship("Sale", back_populates="area", cascade="all, delete-orphan")
    supplier = relationship("Supplier", back_populates="area", cascade="all, delete-orphan")
    cash_register = relationship("cash_register", back_populates="area", cascade="all, delete-orphan")
    stock = relationship("StockMovement", back_populates="area", cascade="all, delete-orphan")