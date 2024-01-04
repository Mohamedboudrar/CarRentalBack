from sqlalchemy.orm import Session
from app import models, utils
from app import schemas, models, utils

def update_password(db: Session, password: str, id: int):
  hashed_pwd = utils.hash_password(password)
  db_user = db.get(models.User, id)
  updated_user = models.User(id=id, password=hashed_pwd)
  setattr(db_user, "password", updated_user.password)
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return {"message": "Password change successful"}
  
def create_user_profile(db: Session, body: schemas.Profile, user_id: int):
  new_profile = models.Profile(user_id=user_id, first_name=body.first_name, last_name=body.last_name)
  db.add(new_profile)
  db.commit()
  db.refresh(new_profile)
  return {"message": "Profile created"}

def handle_update_current_user_profile(db: Session, body: schemas.Profile, user_id: int):
  db_user = db.query(models.Profile).filter(models.Profile.user_id == user_id)
  db_user.update({"first_name": body.first_name, "last_name": body.last_name})
  db.commit()
  return {"message": "Profile has been updated"}