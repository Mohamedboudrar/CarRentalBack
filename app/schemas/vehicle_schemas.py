from pydantic import BaseModel
from enum import Enum
from typing import Optional

class StatusEnum(str, Enum):  # Ensure StatusEnum works smoothly with Pydantic
    available = "available"
    active = "active"
    unavailable = "unavailable"

class AddVehicle(BaseModel):
    name: str
    model: str
    description: str
    price: float  # Changed from str to float for numerical validation
    picture: Optional[str] = None  # Assuming this is a URL or path as a string
    status: StatusEnum
