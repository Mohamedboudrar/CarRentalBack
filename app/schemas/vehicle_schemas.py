from pydantic import BaseModel
from enum import Enum

class StatusEnum(Enum):
    available = "available"
    active = "active"
    unavailable = "unavailable"

class AddVehicle(BaseModel):
    name: str
    model: str
    description: str
    status: StatusEnum
  