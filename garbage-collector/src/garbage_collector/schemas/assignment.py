from pydantic import BaseModel
from datetime import datetime

class BinPickUpAssignmentOutput(BaseModel):
    id: int
    bin_id: int
    truck_id: int
    pickup_status: str
    garbage_quantity: int
    assigned_date: datetime

    class Config:
        from_attributes = True