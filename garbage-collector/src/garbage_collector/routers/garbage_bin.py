from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.garbage_collector.schemas import bin as bin_schema
from src.garbage_collector.services import bin as bin_service
from src.garbage_collector.database.database import get_db

router = APIRouter(prefix="/bin")

@router.post("/add")
def add_bin(bin_data:bin_schema.BinBaseModel, db:Session = Depends(get_db)):
    try:
        response = bin_service.add_bin(bin_data=bin_data, db=db)
        return response
    except Exception as e:
        HTTPException(status_code=500, details=f"Error : {e}")

@router.patch("/add-garbage")
def add_garbage(add_garbage:bin_schema.AddGarbage, db:Session = Depends(get_db)):
    try:
        response = bin_service.add_garbage(add_garbage=add_garbage, db=db)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error : {e}")

@router.get("/all")
def get_all_bins(db:Session = Depends(get_db)):
    try:
        response = bin_service.get_all(db=db)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error : {e}")
        