from fastapi import APIRouter, Depends, HTTPException
import app.schemas.user as schema_user
import app.models.user as model_user
import app.schemas.response_entity as schema_res
from app.core.database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

@router.post("/users")
def create_user(user: schema_user.UserCreate, db: Session = Depends(get_db)):
    db_user = model_user.User(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users", response_model=schema_res.Response[List[schema_user.UserResponse]])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(model_user.User).all()
    return schema_res.Response(code=200, message="success", data=users)

@router.get("/users/{id}", response_model=schema_res.Response[schema_user.UserResponse])
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.get(model_user.User, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return schema_res.Response(code=200, message="success", data=user)