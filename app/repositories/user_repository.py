from sqlalchemy.orm import Session
from sqlalchemy import exists
from fastapi import HTTPException
from app.models.user import User

class UserRepository:

    def exist_user_name(self, username: str, db: Session) -> bool:
        return db.query(
            exists().where(User.username == username)
        ).scalar()

    def exist_user_id(self, user_id: int, db: Session) -> bool:
        return db.query(
            exists().where(User.id == id)
        ).scalar()

    def create(self, user_create, db: Session):
        if self.exist_user_name(user_create.username, db):
            raise ValueError("Username already exists")
        user = User(username=user_create.username, password=user_create.password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def get_all(self, db: Session):
        return db.query(User).all()

    def get_by_id(self, user_id: int, db: Session):
        user = db.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def get_by_username(self, username: str, db: Session):
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user



