"""bcrypt password hashing + JWT bearer auth."""
import os
from datetime import datetime, timedelta, timezone
import bcrypt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from .database import get_db
from .models import User

SECRET = os.getenv("JWT_SECRET")
if not SECRET:
    raise RuntimeError("JWT_SECRET is not set. Copy .env.example to .env and fill it in.")
ALGO = "HS256"
EXPIRE_MIN = int(os.getenv("JWT_EXPIRE_MINUTES", "120"))
oauth2 = OAuth2PasswordBearer(tokenUrl="login")


def hash_password(pw: str) -> str:
    return bcrypt.hashpw(pw.encode()[:72], bcrypt.gensalt()).decode()


def verify_password(pw: str, hashed: str) -> bool:
    return bcrypt.checkpw(pw.encode()[:72], hashed.encode())


def make_token(user_id: int) -> str:
    exp = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MIN)
    return jwt.encode({"sub": str(user_id), "exp": exp}, SECRET, algorithm=ALGO)


def get_current_user(token: str = Depends(oauth2), db: Session = Depends(get_db)) -> User:
    err = HTTPException(401, "Your session has expired. Log in again.", headers={"WWW-Authenticate": "Bearer"})
    try:
        uid = int(jwt.decode(token, SECRET, algorithms=[ALGO])["sub"])
    except (JWTError, KeyError, ValueError):
        raise err
    user = db.get(User, uid)
    if not user:
        raise err
    return user
