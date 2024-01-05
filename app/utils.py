from passlib.context import CryptContext
from datetime import timedelta, datetime
from jose import jwt, JWTError
from app import schemas, models, db
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.config import secret_key, algorithm, access_token_expire_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)
  
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
  
def create_access_token(data: dict, minutes: int = None):
  to_encode = data.copy()
  expire = datetime.utcnow() + timedelta(minutes=access_token_expire_minutes if not minutes else minutes)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
  return encoded_jwt

def verify_token_access(token: str):
  credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                        detail="Could not Validate Credentials. Token is invalid or expired",
                                        headers={"WWW-Authenticate": "Bearer"})
  try:
    payload = jwt.decode(token, secret_key, algorithms=algorithm)
    id: str = payload.get("user_id")
    if id is None:
      raise credentials_exception
    token_data = schemas.DataToken(id=str(id))
  except JWTError as e:
    print(e)
    raise credentials_exception
  return token_data
    
def get_current_user(token: str, db: Session = Depends(db.get_db)):
  token = verify_token_access(token)
  user = db.query(models.User).filter(models.User.id == token.id).first()
  return user