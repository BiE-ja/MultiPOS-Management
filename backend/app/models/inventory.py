from app.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from datetime import datetime, timezone


class StockMovement(Base):
    __tablename__="stock"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    movementType_id = Column(Integer, ForeignKey("movement.id"), nullable=False)
    area_id = Column(Integer, ForeignKey("area.id"), nullable=False)
    quantity = Column(Integer, default=0)
    move_date = Column(DateTime(timezone=True), default=lambda:datetime.now(timezone.utc))
    comment= Column(String) # optional. use for ajustement : reason of ajustement (error of tape, cause of return supplier, cause of return customer, vol, produit périmé, ....)

    area= relationship("Area", back_populates="stock")
    product = relationship("Product", back_populate = "stock")
    movement= relationship("movement", back_populates="stock")

class MovementType(Base):
    __tablename__="movement"
    id=Column(Integer, primary_key=True, index=True)
    name= Column(String, unique = True, nullable=False) # in, out, inventory, ajustement,return_supplier, return_customer

    stock = relationship("StockMovement", back_populates="movementType")
    
    