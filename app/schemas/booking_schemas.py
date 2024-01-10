from pydantic import BaseModel,Field, UUID4
from datetime import date
    
class MakeBooking(BaseModel):
    vehicle_id: UUID4=Field(...)
    start_date: date=Field(...)
    end_date: date=Field(...)
