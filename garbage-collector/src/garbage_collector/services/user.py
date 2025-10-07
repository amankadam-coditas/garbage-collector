from src.garbage_collector.schemas import auth as auth_schema
from sqlalchemy.orm import Session
from src.garbage_collector.models.base import User
from fastapi import HTTPException, status, Depends
from src.garbage_collector.services.auth import (
    hash_password,
    verify_password,
    create_token,
    decode_token,
)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.garbage_collector.database.database import get_db

security = HTTPBearer()


def get_current_user(
    credential: HTTPAuthorizationCredentials = Depends(security), db=Depends(get_db)
):
    token = credential.credentials
    payload_claims = decode_token(token=token)
    return payload_claims


def check_access_role(role_scope):
    def wrapper(payload=Depends(get_current_user)):
        if payload["user_role"] not in role_scope:
            raise HTTPException(403, detail="Insufficient permissions.")

    return wrapper


def add_user(credentials: auth_schema.UserSignIn, db: Session):
    user = db.query(User).filter(User.email == credentials.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists."
        )
    hashed_password = hash_password(credentials.password)
    new_user = User(
        email=credentials.email,
        hashed_password=hashed_password,
        user_role=credentials.role.value,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def login_user(credentials: auth_schema.UserSignIn, db: Session):
    user = db.query(User).filter(User.email == credentials.email).first()
    if user is None:
        raise HTTPException(400, detail="Incorrect email or password.")
    if not verify_password(
        plain_password=credentials.password, hashed_password=user.hashed_password
    ):
        raise HTTPException(400, detail="Incorrect email or password.")
    token = create_token({"sub": str(user.id), "user_role": user.user_role})
    return {"access_token": token, "token_type": "Bearer"}
