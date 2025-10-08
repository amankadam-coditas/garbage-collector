from pydantic import BaseModel, Field
from typing import Optional

class BinBaseModel(BaseModel):
    name: str = Field(...)
    location_id : int = Field(...)
    total_capacity : int = Field(..., gt=0)
    fill_level : int = Field(..., ge=0)
    is_available : Optional[bool] 

    class Config:
        from_attributes = True  

class BinOutput(BinBaseModel):
    id: int

class AddGarbage(BaseModel):
    bin_id:int = Field(...)
    fill_level:int = Field(ge=0)