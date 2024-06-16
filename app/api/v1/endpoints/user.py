from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List

from dependencies import get_db
from schemas.user import User, UserCreate, UserUpdate, ChangePassword, Token, TokenData
from repositories.user import get_user, get_user_by_email, get_users, create_user, update_user, delete_user
from services.email import Util
import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError

router = APIRouter()

@router.post("/register/", response_model=User)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    if user.password != user.password_conf:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    return create_user(db=db, user=user)

@router.post("/login/", response_model=Token)
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_email(db, email=form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not user.hashed_password.endswith(form_data.password + "notreallyhashed"):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = jwt.encode({"sub": user.email}, "SECRET_KEY", algorithm="HS256")
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users

@router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = update_user(db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/users/{user_id}", response_model=User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/users/change-password/", response_model=User)
def change_password(user_id: int, password_data: ChangePassword, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not db_user.hashed_password.endswith(password_data.old_password + "notreallyhashed"):
        raise HTTPException(status_code=400, detail="Old password is incorrect")
    db_user.hashed_password = password_data.new_password + "notreallyhashed"
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/email-verify/")
def verify_email(token: str, db: Session = Depends(get_db)):
    try:
        token_data = jwt.decode(token, "SECRET_KEY", algorithms=["HS256"])
        user = get_user_by_email(db, email=token_data.get("sub"))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not user.is_active:
            user.is_active = True
            db.add(user)
            db.commit()
            db.refresh(user)
        return {"message": "Email successfully verified"}
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")
