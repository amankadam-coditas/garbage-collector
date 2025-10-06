from sqlalchemy import Column, Integer, Float, ForeignKey, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from src.garbage_collector.models.base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, index=True)
    user_role = Column(String, index=True) # user_role = Admin, Supervisor

class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class Bin(Base):
    __tablename__ = "bins"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location_id = Column(Integer, ForeignKey("locations.id"))
    total_capacity = Column(Integer, default=100)
    fill_level = Column(Integer, default=0)
    is_available = Column(Boolean) # Flags -> True means available for Pickup else Not available for Pickup

class Truck(Base):
    __tablename__ = "trucks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    total_capacity = Column(Integer, default=200)
    fill_level = Column(Integer, default=0)
    is_available = Column(Boolean)

class BinPickUpAssignment(Base):
    __tablename__ = "bin_pickup_assignments"
    id = Column(Integer, primary_key=True, index=True)
    bin_id = Column(Integer, ForeignKey("bins.id"))
    truck_id = Column(Integer, ForeignKey("trucks.id"))
    pickup_status = Column(String, default="Assigned") # Pickup Status -> Assigned, Picked, Done
    assigned_date = Column(DateTime, default=func.now())
