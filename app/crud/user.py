from sqlalchemy.orm import Session
from app import models, utils

def update_password(db: Session, password: str, id: int):
  hashed_pwd = utils.hash_password(password)
  db_user = db.get(models.User, id)
  updated_user = models.User(id=id, password=hashed_pwd)
  setattr(db_user, "password", updated_user.password)
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return {"message": "Password change successful"}
  