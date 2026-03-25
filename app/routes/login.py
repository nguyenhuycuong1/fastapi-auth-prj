from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.auth import verify_password, create_token, verify_token
from app.core.database import get_db
from app.models.refresh_token import RefreshToken
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

    token = create_token(data={"sub": user.username}, token_type="access")
    refresh_token = create_token(data={"sub": user.username}, token_type="refresh")

    refresh_payload = verify_token(refresh_token, expected_type="refresh", return_payload=True)
    db.add(
        RefreshToken(
            jti=refresh_payload["jti"],
            user_id=user.id,
            expires_at=datetime.utcfromtimestamp(refresh_payload["exp"]),
        )
    )
    db.commit()

    return {"access_token": token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/refresh")
def refresh_token(token: str, db: Session = Depends(get_db), user_service: UserService = Depends(get_user_service)):
    refresh_payload = verify_token(token, expected_type="refresh", return_payload=True)
    username = refresh_payload["sub"]
    user = user_service.get_user_by_username(username=username, db=db)

    refresh_session = (
        db.query(RefreshToken)
        .filter(RefreshToken.jti == refresh_payload["jti"], RefreshToken.user_id == user.id)
        .first()
    )

    if refresh_session is None or refresh_session.revoked_at is not None:
        raise HTTPException(status_code=401, detail="Invalid token")

    if refresh_session.expires_at <= datetime.utcnow():
        raise HTTPException(status_code=401, detail="Invalid token")

    refresh_session.revoked_at = datetime.utcnow()

    new_access_token = create_token(data={"sub": username}, token_type="access")
    new_refresh_token = create_token(data={"sub": username}, token_type="refresh")
    new_refresh_payload = verify_token(new_refresh_token, expected_type="refresh", return_payload=True)

    db.add(
        RefreshToken(
            jti=new_refresh_payload["jti"],
            user_id=user.id,
            expires_at=datetime.utcfromtimestamp(new_refresh_payload["exp"]),
        )
    )
    db.commit()

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }
