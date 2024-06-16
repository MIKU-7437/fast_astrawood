
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    username: Optional[str] = None
    city: str
    region: str
    address: str
    phone: str
    photo: Optional[str] = "customer_photos/default-profile-picture.jpg"

class UserCreate(UserBase):
    password: str
    password_conf: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDBBase(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class User(UserInDBBase):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class ChangePassword(BaseModel):
    old_password: str
    new_password: str

