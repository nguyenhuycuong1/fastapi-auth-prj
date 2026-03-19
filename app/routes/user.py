from fastapi import APIRouter, Depends, HTTPException
import app.schemas.user as schema_user
from app.core.database import get_db
from sqlalchemy.orm import Session
from typing import List
from app.services import user_service

router = APIRouter()

@router.post("/users", response_model=schema_user.UserResponse)
def create_user(user: schema_user.UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(user, db)

@router.get("/users", response_model=List[schema_user.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return user_service.get_all_users(db)

@router.get("/users/{id}", response_model=schema_user.UserResponse)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    return user_service.get_user_by_id(user_id=id, db=db)