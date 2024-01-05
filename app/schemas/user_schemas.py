from pydantic import BaseModel

class ChangePassword(BaseModel):
  current_password: str
  new_password: str
  
class Profile(BaseModel):
  first_name: str
  last_name: str