from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import Category, CategoryCreate, Product, ProductCreate
from app.repositories import get_category, get_categories, create_category, get_product, get_products, create_product
from app.db.session import get_db

router = APIRouter()

@router.post("/categories/", response_model=Category)
def create_new_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return create_category(db=db, category=category)

@router.get("/categories/{category_id}", response_model=Category)
def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = get_category(db=db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.get("/categories/", response_model=List[Category])
def read_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    categories = get_categories(db=db, skip=skip, limit=limit)
    return categories

@router.post("/products/", response_model=Product)
def create_new_product(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db=db, product=product)

@router.get("/products/{product_id}", response_model=Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = get_product(db=db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.get("/products/", response_model=List[Product])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    products = get_products(db=db, skip=skip, limit=limit)
    return products

