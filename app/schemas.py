from typing import Optional, Generic, TypeVar
from pydantic import BaseModel,Field, EmailStr

T = TypeVar('T')
    
class RequestUser(BaseModel):
  email: Optional[EmailStr]=Field(...)
  password: Optional[str]=Field(...)
  
  class Config:
    from_attributes = True
  
class Response(BaseModel, Generic[T]):
  code: str
  status: str
  message: str
  result: Optional[T]