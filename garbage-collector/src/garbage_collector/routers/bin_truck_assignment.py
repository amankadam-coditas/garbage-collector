from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.garbage_collector.schemas import bin as bin_schema
from src.garbage_collector.services import bin as bin_service
from src.garbage_collector.database.database import get_db


router = APIRouter(prefix="/smart-management")

@router.post("/auto-assign")
def auto_assign_pickup():
    try:
        ...
    except Exception as e:
        ...