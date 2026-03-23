from fastapi import APIRouter, Depends, HTTPException
import app.schemas.user as schema_user
from app.core.auth import get_current_user
from app.core.database import get_db
from sqlalchemy.orm import Session
from typing import List
from app.services.user_service import UserService

def get_user_service():
    return UserService()
router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[
        (Depends(get_db)),
        (Depends(get_user_service)),
        (Depends(get_current_user))
    ]
)

public_router = APIRouter(prefix="/users", tags=["users"])

@public_router.post("/", response_model=schema_user.UserResponse)
def create_user(user: schema_user.UserCreate, db: Session = Depends(get_db), user_service: UserService = Depends(get_user_service)):
    return user_service.create_user(user, db)

@router.get("/", response_model=List[schema_user.UserResponse])
def get_all_users(db: Session = Depends(get_db), user_service: UserService = Depends(get_user_service)):
    return user_service.get_all_users(db)

@router.get("/{id}", response_model=schema_user.UserResponse)
def get_user_by_id(id: int, db: Session = Depends(get_db), user_service: UserService = Depends(get_user_service)):
    return user_service.get_user_by_id(user_id=id, db=db)