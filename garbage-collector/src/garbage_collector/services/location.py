from sqlalchemy.orm import Session
from src.garbage_collector.schemas import location as location_schema
from src.garbage_collector.models.base import Location


def add_location(location_data : location_schema.LocationBase, db: Session):
    new_location = Location(name=location_data.name)
    db.add(new_location)
    db.commit()
    db.refresh(new_location)
    return new_location

def get_all_locations(db:Session):
    all_locations = db.query(Location).all()
    return all_locations