import datetime
from sqlalchemy import Column, DateTime, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone

class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    area_id = Column(Integer, ForeignKey("area.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("productCategory.id"))
    # actual price
    price = Column(Float, nullable = False) # type: ignore
    purchase_price = Column(Float) # type: ignore
    init_stock = Column(Integer)
    actual_stock = Column(Integer)

    area = relationship("Area", back_populates="product")
    productCategory = relationship("ProductCategory", back_populates="product")
    price_history = relationship("PriceHistory", back_populates="product", cascade="all, delete-orphan")
    # for history of stock movement for one product
    stockMovement = relationship("StockMovement", back_populates="product")
    purchase = relationship("Purchase", baback_populates="product")
    SaleDetail = relationship("SaleDetail", baback_populates="product")
    # One supplier can have one or many product to sale
    supplier = relationship("Supplier", back_populates="product")

class ProductCategory(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, index = True)
    cat_name = Column(String, index = True)
    area_id = Column(Integer, ForeignKey("area.id"), nullable=False)

    area = relationship("Area", back_populates="productcategory")
    product = relationship("Product", back_populates="productCategory")

class PriceHistory(Base):
    __tablename__ = "price_history"
    id = Column(Integer, primary_key=True,index=True)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False) 
    type = Column(String) # achat ou vente
    value = Column(Float)  # type: ignore
    date = Column(DateTime(timezone=True), default=lambda:datetime.now(timezone.utc))

    product = relationship("Product", back_populates="priceHistory")
