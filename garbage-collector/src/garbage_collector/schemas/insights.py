from pydantic import BaseModel

class LocationInsight(BaseModel):
    location_name: str
    total_garbage: int