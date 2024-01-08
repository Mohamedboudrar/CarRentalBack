from typing import Optional
from pydantic import BaseModel,Field, EmailStr
from datetime import date
    
class MakeBooking(BaseModel):
    vehicle_id: int=Field(...)
    start_date: date=Field(...)
    end_date: date=Field(...)
