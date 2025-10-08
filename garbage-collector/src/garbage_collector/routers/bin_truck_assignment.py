from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.garbage_collector.schemas import bin as bin_schema
from src.garbage_collector.services import bin as bin_service
from src.garbage_collector.services import smart_management as smart_management_service
from src.garbage_collector.database.database import get_db
from src.garbage_collector.services.user import check_access_role
from typing import List
from src.garbage_collector.schemas.assignment import BinPickUpAssignmentOutput
from src.garbage_collector.schemas.insights import LocationInsight

router = APIRouter(prefix="/smart-management")

@router.post("/auto-assign", dependencies=[Depends(check_access_role("admin"))],
             response_model=List[BinPickUpAssignmentOutput])
def auto_assign_pickup(db:Session = Depends(get_db)):
    try:
        response = smart_management_service.auto_assign_bins(db=db)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error : {e}")

@router.get("/insights/top-locations",
            dependencies=[Depends(check_access_role("admin"))],
            response_model=List[LocationInsight])
def get_top_locations(db: Session = Depends(get_db)):
    """
    Get an ordered list of locations that have generated the most garbage
    in the last 7 days.
    """
    try:
        response = smart_management_service.get_garbage_insights_by_location(db=db)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error : {e}")

@router.patch("/assignments/{assignment_id}/complete",
              dependencies=[Depends(check_access_role(["admin", "driver"]))],
              response_model=BinPickUpAssignmentOutput)
def complete_assignment(assignment_id: int, db: Session = Depends(get_db)):
    """
    Mark a specific pickup assignment as completed. This action updates
    the truck's and bin's fill levels.
    """
    try:
        response = smart_management_service.complete_pickup(assignment_id=assignment_id, db=db)
        return response
    except HTTPException as he:
        raise he # Re-raise HTTPException to preserve status code and detail
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error : {e}")
        