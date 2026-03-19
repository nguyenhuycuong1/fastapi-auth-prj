
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.models.user import User

def create_user(user_create: UserCreate, db: Session):
    user = User(username=user_create.username, password=user_create.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_all_users(db: Session):
    users = db.query(User).all()
    return users

def get_user_by_id(user_id: int, db: Session):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
