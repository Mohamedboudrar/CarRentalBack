from typing import Optional, TypeVar
from pydantic import BaseModel,Field, EmailStr
    
class RequestUser(BaseModel):
  email: Optional[EmailStr]=Field(...)
  password: Optional[str]=Field(...)
  
  class Config:
    from_attributes = True
    
class DataToken(BaseModel):
    id: Optional[str] = None
    
class ForgotPassword(BaseModel):
  email: str
  
class ResetPassword(BaseModel):
  token: str
  password: str
  confirm_password: str

class ValidateForgotPasswordCode(BaseModel):
  token: str