from fastapi import APIRouter, Depends, Response
from app import models, config, crud, schemas
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=config.engine)

router = APIRouter()

def get_db():
  db = config.SessionLocal()
  try:
    yield db
  finally:
    db.close()

@router.post('/register')
async def register(request: schemas.RequestUser, db:Session=Depends(get_db)):
  crud.create_user(db, request)
  return Response(
    status_code=201
  )
  
@router.post('/login')
async def login():
  return {"message": "log in successfull"}

@router.post('/forgot-password')
async def forgot_password():
  return {"message": "Reset link sent to your email address"}


@router.post('/reset-password')
async def rest_password():
  return {"message": "Password reset successful"}

