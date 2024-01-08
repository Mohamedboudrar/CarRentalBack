from pydantic import BaseModel,Field
from datetime import date
    
class MakeBooking(BaseModel):
    vehicle_id: str=Field(...)
    start_date: date=Field(...)
    end_date: date=Field(...)
