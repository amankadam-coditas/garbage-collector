from sqlalchemy.orm import Session
from src.garbage_collector.schemas import location as location_schema
import copy
from src.garbage_collector.models.base import Location, Bin, Truck, BinPickUpAssignment

"""
for bin in data["bins"]:
    print(bin["fill_level"], bin["total_capacity"])
    for truck in data["trucks"]:
        current_capacity_of_truck = truck["total_capacity"] - truck["fill_level"] 
        if current_capacity_of_truck >= bin["fill_level"]:
            truck["fill_level"] += bin["fill_level"]
            bin["fill_level"] = 0
            bin["is_available"] = False 
        elif current_capacity_of_truck < bin["fill_level"]:
            truck["fill_level"] = truck["total_capacity"]
            bin["fill_level"] -= current_capacity_of_truck

"""

def auto_assign_bins(db:Session):
    all_available_bins = db.query(Bin).filter(Bin.is_available == True).all()
    all_available_trucks = db.query(Truck).filter(Truck.is_available == True).all()
    virtual_bins = copy.deepcopy(all_available_bins)
    virtual_trucks = copy.deepcopy(all_available_trucks)
    for bin in virtual_bins:    
        for truck in virtual_trucks:
            current_capacity_of_truck = truck.total_capacity - truck.fill_level
            print("Checking for bin >>>>>",bin.name,current_capacity_of_truck,truck.name, bin.fill_level)
            if truck.is_available and bin.is_available:
                if current_capacity_of_truck >= bin.fill_level:
                    new_assignment = BinPickUpAssignment(bin_id=bin.id, truck_id=truck.id, 
                                                        pickup_status="assigned", garbage_quantity=bin.fill_level)
                    """
                truck["fill_level"] += bin["fill_level"]    
                bin["fill_level"] = 0
                    """
                    truck.fill_level += bin.fill_level
                    bin.fill_level = 0
                    if truck.fill_level == truck.total_capacity:
                        truck.is_available = False
                        truck_info = db.query(Truck).filter(Truck.id == truck.id).first()
                        truck_info.is_available = False
                        db.commit()
                    bin.is_available = False
                    db.add(new_assignment)
                    db.commit()

                elif current_capacity_of_truck < bin.fill_level:
                    
                    new_assignment = BinPickUpAssignment(bin_id=bin.id, truck_id=truck.id, 
                                                        pickup_status="assigned", garbage_quantity=current_capacity_of_truck)
                    """
                truck["fill_level"] = truck["total_capacity"]
                bin["fill_level"] -= current_capacity_of_truck
                    """
                    truck.fill_level += current_capacity_of_truck
                    bin.fill_level -= current_capacity_of_truck
                    if bin.fill_level == 0:
                        bin.is_available = False
                    if truck.fill_level == truck.total_capacity:
                        truck.is_available = False
                        truck_info = db.query(Truck).filter(Truck.id == truck.id).first()
                        truck_info.is_available = False
                        db.commit()
                    db.add(new_assignment)
                    db.commit()

    bin_pickups_schedule = db.query(BinPickUpAssignment).all()
    return bin_pickups_schedule