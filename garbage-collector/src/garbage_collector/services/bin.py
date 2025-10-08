from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.garbage_collector.schemas import bin as bin_schema
from src.garbage_collector.models.base import Bin

def add_bin(bin_data:bin_schema.BinBaseModel, db: Session):
    new_bin = Bin(name=bin_data.name, location_id=bin_data.location_id, total_capacity=bin_data.total_capacity,fill_level=bin_data.fill_level)
    db.add(new_bin)
    db.commit()
    db.refresh(new_bin)
    return new_bin

def add_garbage(add_garbage:bin_schema.AddGarbage, db:Session):
    garbage_bin = db.query(Bin).filter(Bin.id == add_garbage.bin_id).first()
    if garbage_bin is None:
        raise HTTPException(status_code=404, detail="Bin not found.")
    if add_garbage.fill_level > garbage_bin.total_capacity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail=f"Fill level can't be greater that capacity. Total Capacity : {garbage_bin.total_capacity} and Fill Level is : {garbage_bin.fill_level}")
    garbage_bin.fill_level = add_garbage.fill_level
    if add_garbage.fill_level > (garbage_bin.total_capacity*0.8):
        garbage_bin.is_available = True
    db.commit()
    db.refresh(garbage_bin)
    return garbage_bin

def get_all(db:Session):
    all_bins = db.query(Bin).all()
    return all_bins

def get_pending_bins(db: Session):
    pending_bins = db.query(Bin).filter(Bin.is_available == True).all()
    return pending_bins