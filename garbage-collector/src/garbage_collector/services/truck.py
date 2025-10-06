from sqlalchemy.orm import Session
from src.garbage_collector.schemas import truck as truck_schema
from src.garbage_collector.models.base import Truck

"""
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    total_capacity = Column(Integer, default=200)
    fill_level = Column(Integer, default=0)
    is_available = Column(Boolean, default=False)
"""

def add_truck(truck_data:truck_schema.TruckBase, db: Session):
    new_truck = Truck(name=truck_data.name, total_capacity=truck_data.total_capacity, 
                      fill_level = truck_data.fill_level, is_available = truck_data.is_available)
    db.add(new_truck)
    db.commit()
    db.refresh(new_truck)
    return new_truck

def get_all_trucks(db:Session):
    all_trucks = db.query(Truck).all()
    return all_trucks