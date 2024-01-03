from fastapi import APIRouter, Depends, Response, HTTPException, Header, Security
from app import models, config, schemas, utils, db
from sqlalchemy.orm import Session
from app.crud.auth import get_user_by_email, login_user, create_user
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer()

models.Base.metadata.create_all(bind=config.engine)

router = APIRouter()

@router.post('/register')
async def register(request: schemas.RequestUser, db:Session=Depends(db.get_db)):
  db_user = get_user_by_email(db, email=request.email)
  if db_user:
    raise HTTPException(status_code=409, detail="Email already registered")
  create_user(db, request)
  return Response(
    status_code=201
  )
  
@router.post('/login')
async def login(request: schemas.RequestUser, db:Session=Depends(db.get_db)):
  db_user = get_user_by_email(db, email=request.email)
  if not db_user:
    raise HTTPException(status_code=409, detail="Email does not exist")
  verified = utils.verify_password(request.password, db_user.password)
  if not verified:
    raise HTTPException(status_code=401, detail="Incorrect email or password")
  response = login_user(db_user)
  return response

def get_token_header(authorization: str = Header(...)):
    print("Authorization Header:", authorization)
    # You can add custom logic to validate or process the authorization header here
    return authorization

@router.get('/me')
def get_current_user(db:Session=Depends(db.get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
  token = credentials.credentials
  user = utils.get_current_user(token, db)
  return user

@router.post('/forgot-password')
async def forgot_password():
  return {"message": "Reset link sent to your email address"}

@router.post('/reset-password')
async def rest_password():
  return {"message": "Password reset successful"}

