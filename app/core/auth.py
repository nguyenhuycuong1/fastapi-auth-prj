from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from uuid import uuid4

SECRET_KEY="nguyen-huy-cuong-auth-fastapi-prj"
ALGORITHM="HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
TOKEN_TYPES = {"access", "refresh"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)

def hash_password(password: str):
    return pwd_context.hash(password)

def create_token(data: dict, token_type: str):
    to_encode = data.copy()
    if token_type == "access":
        expire = datetime.utcnow() + timedelta(minutes=1)
    elif token_type == "refresh":
        expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"jti": str(uuid4())})
    else:
        raise ValueError("Invalid token type")

    to_encode.update({"exp": expire, "token_type": token_type})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str, expected_type: str | None = None, return_payload: bool = False):
    if expected_type and expected_type not in TOKEN_TYPES:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        token_type: str | None = payload.get("token_type")

        if username is None or token_type not in TOKEN_TYPES:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        if expected_type and token_type != expected_type:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        if token_type == "refresh" and not payload.get("jti"):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        if return_payload:
            return payload
        return username
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    username = verify_token(token, expected_type="access")
    return username