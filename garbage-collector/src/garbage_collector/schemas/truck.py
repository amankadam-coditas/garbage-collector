from pydantic import BaseModel, Field

class TruckBase(BaseModel):
    name : str = Field(..., description="Enter Truck name.")
    total_capacity : int = Field(..., gt=0)
    fill_level : int = Field(..., ge=0)
    is_available : bool = Field(default=True)

    class Config:
        from_attributes = True

class TruckOutput(TruckBase):
    id : int

