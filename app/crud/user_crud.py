from sqlalchemy.orm import Session
from app import models, db
from app.schemas import user_schemas
from fastapi import Depends, Response, status
from app.utils.jwt_utils import verify_token_access
from app.utils.password_utils import hash_password

def update_password(db: Session, password: str, id: str):
  hashed_pwd = hash_password(password)
  db_user = db.get(models.User, id)
  updated_user = models.User(id=id, password=hashed_pwd)
  setattr(db_user, "password", updated_user.password)
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return {"message": "Password change successful"}

def handle_update_current_user_profile(db: Session, body: user_schemas.Profile, user_id: str):
  db_user = db.query(models.User).filter(models.User.id == user_id)
  db_user.update({"first_name": body.first_name, "last_name": body.last_name})
  db.commit()
  return {"message": "Profile has been updated"}

def handle_get_current_user(token: str, db: Session = Depends(db.get_db)):
  token = verify_token_access(token)
  user = db.query(models.User).filter(models.User.id == token.id).first()
  return user

def get_user_profile(response: Response, id: str, db: Session = Depends(db.get_db)):
    profile_exists = db.query(models.User).filter(models.User.id == id).first()
    if not profile_exists:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "profile NOT FOUND"}
    response.status_code = status.HTTP_200_OK
    return profile_exists