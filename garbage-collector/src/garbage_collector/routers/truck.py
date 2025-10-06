from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.garbage_collector.schemas import truck as truck_schema
from src.garbage_collector.database.database import get_db
from src.garbage_collector.services import truck as truck_service

router = APIRouter(prefix="/truck")

@router.post("/add", response_model=truck_schema.TruckOutput)
def add_truck(truck_data : truck_schema.TruckBase, db : Session = Depends(get_db)):
    try:
        response = truck_service.add_truck(truck_data=truck_data, db=db)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error : {e}")

@router.get("/all")
def get_all_trucks(db:Session = Depends(get_db)):
    try:
        response = truck_service.get_all_trucks(db=db)
        return response
    except Exception as e:
        HTTPException(status_code=500, detail=f"Error : {e}")