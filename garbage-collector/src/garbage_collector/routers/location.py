from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.garbage_collector.schemas import location as location_schema
from src.garbage_collector.database.database import get_db
from src.garbage_collector.services import location as location_service

router = APIRouter(prefix="/location")

@router.post("/add", response_model=location_schema.LocationOutput)
def add_location(location_data : location_schema.LocationBase, db : Session = Depends(get_db)):
    try:
        response = location_service.add_location(location_data=location_data, db=db)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error : {e}")

@router.get("/all")
def get_all_locations(db:Session = Depends(get_db)):
    try:
        response = location_service.get_all_locations(db=db)
        return response
    except Exception as e:
        HTTPException(status_code=500, detail=f"Error : {e}")