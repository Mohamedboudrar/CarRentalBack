from sqlalchemy.orm import Session
from app import schemas, models, utils
from datetime import timedelta, datetime
from typing import Union
from jose import jwt
import os
from ..utils import create_access_token
from dotenv import load_dotenv

load_dotenv()

secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")
access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

def create_user(db: Session, body: schemas.RequestUser):
  hashed_pwd = utils.hash_password(body.password)
  new_user = models.User(email=body.email, password=hashed_pwd)
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user

def login_user(user: models.User):
  access_token = create_access_token(
    data={"user_id": user.id}
  )
  return {"access_token": access_token, "token_type": "bearer"}

def get_user_by_email(db: Session, email: str):
  return db.query(models.User).filter(models.User.email == email).first()