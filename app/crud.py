from sqlalchemy.orm import Session
from app import schemas, models, utils

def create_user(db: Session, body: schemas.RequestUser):
  hashed_pwd = utils.hash_password(body.password)
  new_user = models.User(email=body.email, password=hashed_pwd)
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user