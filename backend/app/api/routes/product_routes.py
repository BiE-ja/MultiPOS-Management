from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from backend.app.api.deps import get_current_user, SessionDep, CurrentUser
from backend.app.crud import product_crud
from backend.app.schemas import product_schema


router = APIRouter()

@router.post("/", response_model= product_schema.ProductRead)
def create_product(product_new: product_schema.ProductCreate, db : SessionDep, user : CurrentUser):  
    return product_crud.create_product(db, product_new)

@router.get("/{product_id}", response_model=product_schema.ProductRead)
def read_product(product_id:int, db: SessionDep, user : CurrentUser): 
    product = product_crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail = "Product not found")
    return product

@router.put("/{product_id}", response_model = product_schema.ProductRead)
def update_product(product_id:int, product_updated : product_schema.ProductUpdate, db:SessionDep,user = Depends(get_current_user)): # type: ignore
    product = product_crud.update_product(db, product_id, product_updated)
    if not product:
        raise HTTPException(status_code=404, detail = "Product not found")
    return product

@router.get("/", response_model=list[product_schema.ProductRead])
def list_all(skip:int =0, limit:int=10, db:Session= Depends(get_db),user = Depends(get_current_user)):# type: ignore
    return product_crud.list_products(db, skip=skip, limit=limit)