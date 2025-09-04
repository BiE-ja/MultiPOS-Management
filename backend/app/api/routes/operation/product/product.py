from fastapi import APIRouter, HTTPException
from app.api.dependencies import CurrentSuperUser, SessionDep, CurrentUserDep, verify_area_access
from app.crud.operation_crud import ProductManager
from app.models.operation.product import PriceType
from app.schemas.operation import product_schema

router = APIRouter(prefix="/product", tags=["product"])

# Product
@router.post("/", response_model= product_schema.ProductRead)
async def create(product_new: product_schema.ProductCreate, db : SessionDep, user : CurrentUserDep):  
    verify_area_access(product_new.area_id, user)
    product = await ProductManager(db).create_product(product_new)
    return product

@router.get("/{product_id}", response_model=product_schema.ProductRead)
async def read(product_id:int, db: SessionDep, user : CurrentUserDep): 
    try:
        product = await ProductManager(db).get_product(product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    verify_area_access(product.area_id, user)
    return product

@router.put("/{product_id}", response_model = product_schema.ProductRead)
async def update(product_id:int, product_updated : product_schema.ProductUpdate, db:SessionDep,user : CurrentUserDep): 
    area_id = product_updated.area_id
    if not area_id:
        product_db = await ProductManager(db).get_product(product_id)
        area_id = product_db.area_id
    verify_area_access(area_id, user)
    product_updated.updated_by_id = user.id
    try:
        product = await ProductManager(db).update_product(product_id, product_updated)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return product

@router.get("/list/{area_id}", response_model=list[product_schema.ProductRead])
async def fetch_all(area_id:int, db: SessionDep, user: CurrentUserDep, skip: int = 0, limit : int =10):
    """Obtain list of product of an area"""
    verify_area_access(area_id, user)
    return await ProductManager(db).get_area_products(area_id, skip, limit)

@router.delete("/{product_id}", status_code=204)
async def delete (area_id:int, product_id:int, db: SessionDep, user: CurrentUserDep):
    verify_area_access(area_id, user)
    try:
        await ProductManager(db).delete_product(product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail = str(e))

@router.get("/superuser/list/{area_id}", response_model=list[product_schema.ProductRead])
async def fetch_all_for_superuser(area_id: int, db: SessionDep, user : CurrentSuperUser,skip: int = 0, limit : int =10):
    """Superuser can obtain list of product for one point of sale"""
    return await ProductManager(db).get_area_products(area_id, skip, limit)

@router.get("/dashbord/", response_model=list[product_schema.ProductDashbordRead])
async def dashboard(area_id:int, db: SessionDep, user: CurrentUserDep, skip: int = 0, limit : int =10):
    verify_area_access(area_id, user)
    # Récupération liste produits

    # Récupération des achats en cours

    # Récupération des commandes clients en cours

    # création d'un ProductDasbordRead et l'ajouter à la liste

    # on retourne la liste
    return

@router.get("/price-history/{product_id}", response_model = list[product_schema.PriceHistoryRead])
async def price_history(area_id:int, product_id:int,type:PriceType, db: SessionDep, user: CurrentUserDep, skip: int = 0, limit : int =10):
    verify_area_access(area_id, user)
    return await ProductManager(db).get_product_history_price(product_id,type, skip, limit)