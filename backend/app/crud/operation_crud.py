import datetime
from sqlalchemy import and_, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.operation.product import (
    PriceHistory, PriceType, Product, ProductCategory, ProductCreationState
    )
from app.models.operation.stock import (
    MovementDirection,
    StockMovement, MovementOperation
    )
from app.schemas.operation.stock_schema import StockMovementCreate
from app.schemas.operation.product_schema import (
    ProductCategoryBase, ProductCategoryUpdate, ProductCreate, ProductUpdate
    )

class ProductManager:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _get_or_create_category(self, product: ProductCreate):
        normalize_category_name = product.category_name.lower() if product.category_name else None
        statement = select(ProductCategory).filter(
            func.lower(ProductCategory.cat_name) == normalize_category_name,
            ProductCategory.area_id == product.area_id
        )
        result = await self.db.execute(statement)
        # Check if the category already exists
        category = result.scalars().first()
        # If it doesn't exist, create a new category    
        if not category:
            category = ProductCategory(cat_name=normalize_category_name, area_id=product.area_id)
            self.db.add(category)
            await self.db.flush()  # Ensure the category is added before creating the product
        return category

    async def create_product(self, data: ProductCreate):
        category = await self._get_or_create_category(data)
        db_prod = Product(
            reference=data.reference,
            name=data.name,
            description=data.description,
            state = ProductCreationState.PENDING,
            price= data.purchase_price,
            purchase_price=data.purchase_price,
            init_stock=data.init_stock or 0,
            actual_stock=data.actual_stock or 0,
            area_id=data.area_id,
            category_id = category.id
        )
        self.db.add(db_prod)
        try:
            await self.db.commit()
        except InterruptedError:
            await self.db.rollback()
            raise ValueError("Product with this reference already exists.")
        await self.db.refresh(db_prod)
        return db_prod
    
    async def update_product(self, product_id:int, data: ProductUpdate) -> Product:
        # Fetch the product to update
        # If product not found, raise an error
        product_db = await self.db.get(Product, product_id)
        # If product not found, raise an error
        if not product_db:
            raise ValueError("Product not found")
        # Create a list to hold price history entries
        history_entries: list[PriceHistory] = []
        # Check if the price or purchase_price has changed
        # If they have, create a PriceHistory entry 
        if data.purchase_price is not None and product_db.purchase_price != data.purchase_price:
            history_entries.append(PriceHistory(
                product_id=product_id,
                type=PriceType.PURCHASE,
                old_value=product_db.purchase_price,
                new_value=data.purchase_price,
                created_by_id=data.updated_by_id,  # Assuming created_by_id is passed in the update
                create_at=  datetime.datetime.now(datetime.timezone.utc),
                comment=getattr(data, 'comment', None)
            ))
        if data.sale_price is not None and product_db.sale_price != data.sale_price:
            history_entries.append(PriceHistory(
                product_id=product_id,
                type=PriceType.SALE,
                old_value=product_db.sale_price,
                new_value=data.sale_price,
                created_by_id=data.updated_by_id,  # Assuming created_by_id is passed in the update
                create_at=  datetime.datetime.now(datetime.timezone.utc),
                comment=getattr(data, 'comment', None)
            ))
        # Update the product fields
        for var, value in data.model_dump(exclude_unset=True).items():
            setattr(product_db, var, value)
        # Add the price history entries to the session
        for history in history_entries: 
            self.db.add(history)
            
        await self.db.commit()
        await self.db.refresh(product_db)
        return product_db
    
    async def get_product(self, product_id: int) -> Product:
        product = await self.db.get(Product, product_id)
        if not product:
            raise ValueError("Product not found")
        return product

    async def delete_product(self, product_id: int):
        product = self.get_product(product_id)
        await self.db.delete(product)
        await self.db.commit()  
    
    async def validate_product(self, product_id : int, validation : ProductCreationState):
        product_db = await self.db.get(Product, product_id)
        if not product_db:
            raise ValueError("Product not found")
        product_db.state = validation
        await self.db.commit()
        await self.db.refresh(product_db)
        return product_db
    
    # to launch periodly : end of day, week or mounth
    async def clean_product_db(self):
        stmt = select(Product).where(Product.state == ProductCreationState.REJECTED)
        result = await self.db.execute(stmt)
        products_to_delete = result.scalars().all()
        await self.db.delete(product for product in products_to_delete)
        await self.db.commit()

    async def delete_category(self, category_id: int):
        category = await self.db.get(ProductCategory, category_id)
        # If category not found, raise an error
        if not category:
            raise ValueError("Category not found")
        # Detach products from this category before deleting
        await self.detach_product_from_category(category_id)
        # Delete the category
        await self.db.delete(category)
    
    async def detach_product_from_category(self, category_id: int):
        # Detach all products from the category
        # This will set the category_id of all products in this category to None
        stmt =(
            update(Product)
            .where(Product.category_id == category_id)
            .values(category_id=None)
        )
        await self.db.execute(stmt)
        await self.db.commit()

    # return a list of all product for area passed in parameter
    async def get_area_products(self, area_id:int, skip:int=0, limit:int=10):
        stmt = (
            select(Product)
            .where(Product.area_id == area_id)
            .order_by(Product.name)
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    # return a list of all product categories for area passed in parameter
    async def get_area_product_categories(self, area_id : int, skip: int=0, limit: int = 10):
        stmt = (
            select(ProductCategory)
            .where(ProductCategory.area_id == area_id)
            .order_by(ProductCategory.cat_name)
            .offset(skip)
            .limit(limit)
        )
        resultat = await self.db.execute(stmt)
        return resultat.scalars().all()

    async def create_category(self, category: ProductCategoryBase):
        db_prod = ProductCategory(**category.model_dump())
        self.db.add(db_prod)
        await self.db.commit()
        await self.db.refresh(db_prod)
        return db_prod
    
    async def get_productCategory(self, category_id: int):
        statement = select(ProductCategory).filter(ProductCategory.id == category_id)
        result = await self.db.execute(statement)
        return result.scalars().first()
    
    async def update_productCategory(self, category_id: int, category_update: ProductCategoryUpdate):
        category_db = await self.db.get(ProductCategory, category_id)
        if category_db:
            for var, value in category_update.model_dump(exclude_unset=True).items():
                setattr(category_db, var, value)
            await self.db.commit()
            await self.db.refresh(category_db)
        return category_db

    async def get_product_history_price(self, product_id: int, type: PriceType, skip: int = 0, limit: int = 10):
        satement = (
            select(PriceHistory)
            .where((PriceHistory.product_id == product_id) & (PriceHistory.type == type))
            .order_by(PriceHistory.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(satement)
        return result.scalars().all()

class StockManager:
    def __init__(self, db: AsyncSession):
        self.db = db    

    def _create_stockMovement(self,data : StockMovementCreate):
        if data.dateof == None :
            data.dateof = datetime.datetime.now(datetime.timezone.utc)
        return StockMovement(
            area_id = data.area_id,
            product_id = data.product_id,
            direction = data.direction,
            operation = data.operation,
            quantity = data.quantity,
            dateof = data.dateof,
            create_at = datetime.datetime.now(datetime.timezone.utc),
            itiated_by_id = data.initiated_by,
            create_by_id = data.created_by,
            comment = getattr(data, 'comment', None)
        )
    
    def _update_fields(self, stock : StockMovement, operation_id : int):
        if stock.operation == MovementOperation.SALE or stock.operation ==MovementOperation.RETURN_CUSTOMER:
            stock.sale_id = operation_id
        elif stock.operation == MovementOperation.SUPPLY or stock.operation == MovementOperation.RETURN_SUPPLIER:
            stock.purchase_id = operation_id
        return stock
        
    async def _update_product_stock_fields(self, stock : StockMovement):
        product_db = await ProductManager(self.db).get_product(stock.product_id)
        product_db.old_stock = product_db.actual_stock
        quantity_movement = stock.quantity 
        if stock.direction == MovementDirection.OUT:
            quantity_movement *= -1
        product_db.actual_stock += quantity_movement
        return product_db

    async def update_stock(self, data : StockMovementCreate):
        stock = self._update_fields(self._create_stockMovement(data), data.operation_id)
        # update the stock in product
        product_db = await self._update_product_stock_fields(stock)
        self.db.add(stock)
        await self.db.flush()
        self.db.add(product_db)
        await self.db.commit()
        await self.db.refresh(stock)
        await self.db.refresh(product_db)
        return stock
    
    async def get_stock_movement(self, stock_movement_id: int):
        stock_movement = self.db.get(StockMovement, stock_movement_id)
        if not isinstance(stock_movement, StockMovement):
            raise ValueError("Stock movement not found")
        return stock_movement
    
    # a movement of stock can be canceled only at the day who his created
    # else, enter a new stock movement exacte oposite of movement to canceled
    async def cancel_movement_stock(self, movement_id:int):
        db_movement = await self.get_stock_movement(movement_id)
        dateofDay = datetime.datetime.today
        if db_movement.create_at != dateofDay:
            raise ValueError("Movement at stock can be cancelled only at the day when his created\n Please procced to a movement opposite")
        # make the operation direction to this opposite
        if db_movement.direction == MovementDirection.IN:
            db_movement.direction = MovementDirection.OUT
        elif db_movement.direction == MovementDirection.OUT:
            db_movement.direction = MovementDirection.IN
        # delete movement in database
        await self.db.delete(db_movement)
        # update the quantity stock labeled in the product
        product_db = await self._update_product_stock_fields(db_movement)
        self.db.add(product_db)
        await self.db.commit()
        await self.db.refresh(product_db)
        return None

    async def product_stock_track(self, product_id:int, area_id:int, date_begin: datetime.datetime, date_end: datetime.datetime, skip:int=0, limit:int=10) :
        statement = (select(StockMovement)
                     .where(
                         and_(
                             StockMovement.area_id == area_id,
                             StockMovement.product_id == product_id,
                             StockMovement.dateOf.between(date_begin, date_end)
                         ))
                     .order_by(StockMovement.dateof.desc())  
                     .offset(skip)
                     .limit(limit)
                     )   
        result = await self.db.execute(statement)
        return result.scalars().all()

