from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.garbage_collector.schemas import bin as bin_schema
from src.garbage_collector.services import bin as bin_service
from src.garbage_collector.services import smart_management as smart_management_service
from src.garbage_collector.database.database import get_db
from src.garbage_collector.services.user import check_access_role


router = APIRouter(prefix="/smart-management")

@router.post("/auto-assign", dependencies=[Depends(check_access_role("admin"))])
def auto_assign_pickup(db:Session = Depends(get_db)):
    try:
        response = smart_management_service.auto_assign_bins(db=db)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error : {e}")