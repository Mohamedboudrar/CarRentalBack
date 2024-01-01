from fastapi import APIRouter, Depends, Response, HTTPException
from app import models, config, crud, schemas, utils
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
  db_user = crud.get_user_by_email(db, email=request.email)
  if db_user:
    raise HTTPException(status_code=409, detail="Email already registered")
  crud.create_user(db, request)
  return Response(
    status_code=201
  )
  
@router.post('/login')
async def login(request: schemas.RequestUser, db:Session=Depends(get_db)):
  db_user = crud.get_user_by_email(db, email=request.email)
  if not db_user:
    raise HTTPException(status_code=409, detail="Email does not exist")
  verified = utils.verify_password(request.password, db_user.password)
  if not verified:
    raise HTTPException(status_code=401, detail="Incorrect email or password")
  response = crud.login_user(db_user)
  return response

@router.post('/forgot-password')
async def forgot_password():
  return {"message": "Reset link sent to your email address"}


@router.post('/reset-password')
async def rest_password():
  return {"message": "Password reset successful"}

