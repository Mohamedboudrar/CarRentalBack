from datetime import timedelta, datetime
from jose import jwt, JWTError
from app.schemas import auth_schemas
from fastapi import HTTPException, status
from app.config import secret_key, algorithm, access_token_expire_minutes

      
def create_access_token(data: dict, minutes: int = None):
    uuid_string = str(data['user_id'])
    data = {'user_id': uuid_string} # reassign user_id value
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=access_token_expire_minutes if not minutes else minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt

def verify_access_token(token: str):
  credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                        detail="Could not Validate Credentials. Token is invalid or expired",
                                        headers={"WWW-Authenticate": "Bearer"})
  try:
      payload = jwt.decode(token, secret_key, algorithms=algorithm)
      id: str = payload.get("user_id")
      if id is None:
          raise credentials_exception
      token_data = auth_schemas.DataToken(id=str(id))
  except JWTError as e:
      print(e)
      raise credentials_exception
  return token_data