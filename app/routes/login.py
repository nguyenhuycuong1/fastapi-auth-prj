from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import verify_password, create_access_token
from app.core.database import get_db
from app.services.user_service import UserService

router = APIRouter()

def get_user_service():
    return UserService()

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db), user_service: UserService = Depends(get_user_service)):
    username: str = form_data.username
    password: str = form_data.password

    user = user_service.get_user_by_username(username=username, db=db)
    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
