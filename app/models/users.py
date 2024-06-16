from sqlalchemy import Column, String, Boolean, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String)
    username = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=False)
    city = Column(String, nullable=False)
    region = Column(String, nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    photo = Column(String, default="customer_photos/default-profile-picture.jpg")
