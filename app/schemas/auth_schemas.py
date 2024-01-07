from typing import Optional
from pydantic import BaseModel,Field, EmailStr
    
class RequestUser(BaseModel):
    email: EmailStr=Field(...)
    password: str=Field(...)
    
class DataToken(BaseModel):
    id: Optional[str] = None
    
class ForgotPassword(BaseModel):
    email: EmailStr=Field(...)
  
class ResetPassword(BaseModel):
    token: str
    password: str=Field(...)
    confirm_password: str=Field(...)

class ValidateForgotPasswordCode(BaseModel):
    token: str