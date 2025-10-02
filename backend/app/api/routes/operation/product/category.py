import uuid
from fastapi import APIRouter, HTTPException
from app.api.dependencies import SessionDep, CurrentUserDep, verify_area_access
from app.dto.crud.operation_crud import ProductManager
from app.dto.schemas.operation import product_schema

router = APIRouter(prefix="/product", tags=["categories"])


# Categories
@router.post("/category/", response_model=product_schema.ProductCategoryRead)
async def create(category_new: product_schema.ProductCategoryCreate, db: SessionDep, user: CurrentUserDep):
    return await ProductManager(db).create_category(category_new)


@router.get("/category/{category_id}", response_model=product_schema.ProductCategoryRead)
async def read(category_id: uuid.UUID, db: SessionDep, user: CurrentUserDep):
    try:
        category = await ProductManager(db).get_productCategory(category_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return category


@router.put("/category/{category_id}", response_model=product_schema.ProductCategoryRead)
async def update(
    category_id: uuid.UUID, category_updated: product_schema.ProductCategoryUpdate, db: SessionDep, user: CurrentUserDep
):
    try:
        category = await ProductManager(db).update_productCategory(category_id, category_updated)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return category


@router.get("/category-list/{area_id}", response_model=list[product_schema.ProductCategoryRead])
async def fetch_all(area_id: int, db: SessionDep, user: CurrentUserDep, skip: int = 0, limit: int = 10):
    return await ProductManager(db).get_area_product_categories(area_id, skip, limit)


@router.delete("/category/{category_id}", status_code=204)
async def delete(area_id: uuid.UUID, category_id: uuid.UUID, session: SessionDep, user: CurrentUserDep):
    verify_area_access(area_id, user)
    try:
        await ProductManager(session).delete_category(category_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
