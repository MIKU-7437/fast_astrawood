from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class Category(Base):
    __tablename__ = 'categories'  # Добавьте эту строку

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    sub_categories = relationship("Category", back_populates="parent_category", remote_side=[id])
    is_subcategory = Column(Boolean, default=False)
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = 'products'  # Добавьте эту строку

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    price = Column(Integer, nullable=False)
    is_available = Column(Boolean, default=True)
    description = Column(String, nullable=True)
    stock = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey('categories.id'))  # Убедитесь, что ForeignKey указывает на правильную таблицу
    category = relationship("Category", back_populates="products")
    created_date = Column(DateTime, default=datetime.utcnow)
    modified_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    photo = Column(String, nullable=True)
