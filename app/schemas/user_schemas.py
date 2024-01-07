from pydantic import BaseModel, Field

class ChangePassword(BaseModel):
    current_password: str=Field(...)
    new_password: str=Field(...)
  
class Profile(BaseModel):
    first_name: str
    last_name: str