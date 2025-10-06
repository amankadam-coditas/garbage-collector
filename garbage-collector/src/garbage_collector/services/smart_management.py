from sqlalchemy.orm import Session
from src.garbage_collector.schemas import location as location_schema
from src.garbage_collector.models.base import Location, Bin, Truck, BinPickUpAssignment

def auto_assign_bins(db:Session):
    
    ...