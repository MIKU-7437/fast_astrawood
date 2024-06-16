from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class CategoryBase(BaseModel):
    title: str
    slug: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    is_subcategory: bool
    sub_categories: List['Category'] = []
    
    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    title: str
    slug: str
    price: int
    description: Optional[str] = None
    is_available: bool = True
    stock: int
    category_id: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    created_date: datetime
    modified_date: datetime
    photo: Optional[str] = None
    
    class Config:
        orm_mode = True
