from typing import Optional, Generic, TypeVar
from pydantic import BaseModel,Field, EmailStr

T = TypeVar('T')
    
class RequestUser(BaseModel):
  email: Optional[EmailStr]=Field(...)
  password: Optional[str]=Field(...)
  
  class Config:
    from_attributes = True

class DataToken(BaseModel):
    id: Optional[str] = None

class ChangePassword(BaseModel):
  current_password: str
  new_password: str
  
class Profile(BaseModel):
  first_name: str
  last_name: str