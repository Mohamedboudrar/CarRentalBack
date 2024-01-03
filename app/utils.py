from passlib.context import CryptContext
from datetime import timedelta, datetime
from jose import jwt, JWTError
import os
from dotenv import load_dotenv
from app import schemas, models, db
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session


load_dotenv()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')
secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")
access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)
  
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
  
def create_access_token(data: dict):
  to_encode = data.copy()
  expire = datetime.utcnow() + timedelta(minutes=access_token_expire_minutes)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
  return encoded_jwt

def verify_token_access(token: str, credentials_exception):
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
  credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                        detail="Could not Validate Credentials",
                                        headers={"WWW-Authenticate": "Bearer"})
  token = verify_token_access(token, credentials_exception)
  user = db.query(models.User).filter(models.User.id == token.id).first()
  return user