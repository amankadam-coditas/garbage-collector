from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from src.garbage_collector.schemas import auth as auth_schema
from sqlalchemy.orm import Session
from src.garbage_collector.database.database import get_db
from urllib.parse import urlencode
from src.garbage_collector.services import user as user_service
from src.garbage_collector.core.config import setting


router = APIRouter(prefix="/auth")


@router.post("/register", response_model=auth_schema.UserOutput)
def sign_up(user_credentials: auth_schema.UserSignIn, db: Session = Depends(get_db)):
    try:
        response = user_service.add_user(user_credentials, db)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error : {e}")


@router.post("/login")
def sign_in(user_credentials: auth_schema.UserSignIn, db: Session = Depends(get_db)):
    try:
        response = user_service.login_user(user_credentials, db)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error : {e}")


# @router.get("/me", dependencies=[Depends(user_service.get_current_user)])
# def greet_me():
#     try:
#         return "Hey there.. whatsupp..."
#     except Exception as e:
#  