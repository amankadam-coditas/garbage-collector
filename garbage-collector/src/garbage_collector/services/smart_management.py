# The final, most efficient, and stateful implementation with partial pickups

from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import status, HTTPException
from src.garbage_collector.models.base import Bin, Truck, BinPickUpAssignment, Location
from datetime import timedelta, datetime

def auto_assign_bins(db: Session):
    """
    Plans pickups with stateful, robust logic that allows for PARTIAL pickups
    to maximize truck capacity.
    """
    
    # === STEP 1: CALCULATE "IN-FLIGHT" CAPACITY (No changes here) ===
    in_flight_garbage_query = db.query(
        BinPickUpAssignment.truck_id,
        func.sum(BinPickUpAssignment.garbage_quantity).label("in_flight_total")
    ).filter(
        BinPickUpAssignment.pickup_status == "assigned"
    ).group_by(
        BinPickUpAssignment.truck_id
    ).all()
    in_flight_garbage_map = {truck_id: total for truck_id, total in in_flight_garbage_query}

    # === STEP 2: INITIALIZE PLANNER WITH TRUE CAPACITY (No changes here) ===
    available_trucks = db.query(Truck).filter(Truck.is_available == True).all()
    truck_planned_capacity = {}
    for truck in available_trucks:
        current_fill = truck.fill_level
        in_flight_load = in_flight_garbage_map.get(truck.id, 0)
        true_available_capacity = truck.total_capacity - current_fill - in_flight_load
        if true_available_capacity > 0:
            truck_planned_capacity[truck.id] = true_available_capacity

    # === STEP 3: ASSIGN BINS (Bin-Centric Loop with NEW Logic) ===
    bins_needing_pickup = db.query(Bin).filter(Bin.is_available == True).order_by(Bin.fill_level.desc()).all()
    
    new_assignments = []
    # We now track how much of each bin has been planned for pickup
    planned_bin_pickup_amount = {}

    for bin_to_assign in bins_needing_pickup:
        # Calculate how much garbage is still left to be planned for this bin
        garbage_left_in_bin = bin_to_assign.fill_level - planned_bin_pickup_amount.get(bin_to_assign.id, 0)
        
        if garbage_left_in_bin <= 0:
            continue # This bin has already been fully planned for pickup

        for truck_id, remaining_capacity in truck_planned_capacity.items():
            if remaining_capacity <= 0:
                continue # This truck is virtually full

            # --- MODIFIED LOGIC BLOCK ---

            if remaining_capacity >= garbage_left_in_bin:
                # Case 1: FULL Pickup (or remaining part)
                pickup_amount = garbage_left_in_bin
                assignment = BinPickUpAssignment(
                    bin_id=bin_to_assign.id, truck_id=truck_id,
                    pickup_status="assigned", garbage_quantity=pickup_amount
                )
                new_assignments.append(assignment)
                
                # Update truck and bin virtual states
                truck_planned_capacity[truck_id] -= pickup_amount
                planned_bin_pickup_amount[bin_to_assign.id] = bin_to_assign.fill_level # Mark bin as fully planned
                break # Bin is fully handled, move to the next bin

            elif remaining_capacity < garbage_left_in_bin:
                # Case 2: PARTIAL Pickup
                pickup_amount = remaining_capacity # Truck takes what it can
                assignment = BinPickUpAssignment(
                    bin_id=bin_to_assign.id, truck_id=truck_id,
                    pickup_status="assigned", garbage_quantity=pickup_amount
                )
                new_assignments.append(assignment)

                # Update truck and bin virtual states
                truck_planned_capacity[truck_id] = 0 # Truck is now full
                planned_bin_pickup_amount[bin_to_assign.id] = planned_bin_pickup_amount.get(bin_to_assign.id, 0) + pickup_amount
                # DO NOT break. Continue looping to see if another truck can take the rest of this bin's garbage.

    # === STEP 4: COMMIT THE NEW PLAN TO THE DATABASE ===
    # We only mark bins as unavailable if they have been fully planned for.
    fully_planned_bin_ids = [
        bin_id for bin_id, amount in planned_bin_pickup_amount.items() 
        if amount >= db.query(Bin.fill_level).filter(Bin.id == bin_id).scalar()
    ]

    if new_assignments:
        if fully_planned_bin_ids:
            db.query(Bin).filter(Bin.id.in_(fully_planned_bin_ids)).update(
                {"is_available": False}, synchronize_session=False
            )
        db.add_all(new_assignments)
        db.commit()

    return new_assignments

def get_garbage_insights_by_location(db: Session):
    """
    Calculates the total garbage collected from each location in the last 7 days.
    This query assumes that a pickup is counted when its status is 'done'.
    """
    seven_days_ago = datetime.utcnow() - timedelta(days=7)

    # This query joins assignments, bins, and locations, groups by location,
    # and sums up the garbage quantity.
    results = db.query(
        Location.name,
        func.sum(BinPickUpAssignment.garbage_quantity).label("total_garbage_collected")
    ).join(
        Bin, Location.id == Bin.location_id
    ).join(
        BinPickUpAssignment, Bin.id == BinPickUpAssignment.bin_id
    ).filter(
        BinPickUpAssignment.assigned_date >= seven_days_ago,
        # Optional: You might want to only count 'done' pickups for accurate historical data
        # BinPickUpAssignment.pickup_status == 'done' 
    ).group_by(
        Location.name
    ).order_by(
        func.sum(BinPickUpAssignment.garbage_quantity).desc()
    ).all()

    # Convert the list of tuples into a list of dictionaries that match the Pydantic schema
    return [{"location_name": name, "total_garbage": total} for name, total in results]

def complete_pickup(assignment_id: int, db: Session):
    """
    Marks a pickup assignment as 'done'.
    This is the execution step:
    1. Updates the truck's real fill_level.
    2. Updates the bin's fill_level to 0.
    """
    # Find the specific assignment
    assignment = db.query(BinPickUpAssignment).filter(BinPickUpAssignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found.")

    # Prevent re-completing an already completed task
    if assignment.pickup_status != 'assigned':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Assignment already has status: {assignment.pickup_status}")

    # Get the related truck and bin
    truck = db.query(Truck).filter(Truck.id == assignment.truck_id).first()
    bin_obj = db.query(Bin).filter(Bin.id == assignment.bin_id).first()
    
    if not truck or not bin_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated truck or bin not found.")

    # --- Perform the state updates ---
    # 1. Update Truck: Add the collected garbage to its real fill level
    truck.fill_level += assignment.garbage_quantity
    
    # 2. Update Bin: The collected portion is now gone
    bin_obj.fill_level -= assignment.garbage_quantity
    if bin_obj.fill_level < 0:
        bin_obj.fill_level = 0 # Ensure it doesn't go below zero

    # 3. Update Assignment: Mark as complete
    assignment.pickup_status = 'done'
    
    db.commit()
    db.refresh(assignment)
    return assignment