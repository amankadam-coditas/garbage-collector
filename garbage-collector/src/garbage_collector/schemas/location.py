from pydantic import BaseModel, Field

class LocationBase(BaseModel):
    name : str = Field(..., description="Enter Location name.")

    class Config:
        from_attributes = True

class LocationOutput(LocationBase):
    id : int