from fastapi import APIRouter, Depends, Response, HTTPException, Header, Security, status
from app import models, schemas, utils, db
from sqlalchemy.orm import Session
from app.crud.auth import get_user_by_email, login_user, create_user, handle_forgot_pwd_req, reset_user_password
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer()

models.Base.metadata.create_all(bind=db.engine)

router = APIRouter()

@router.post('/register')
async def register(request: schemas.RequestUser, db:Session=Depends(db.get_db)):
  db_user = get_user_by_email(db, email=request.email)
  if db_user:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
  create_user(db, request)
  return Response(
    status_code=201
  )
  
@router.post('/login')
async def login(request: schemas.RequestUser, db:Session=Depends(db.get_db)):
  db_user = get_user_by_email(db, email=request.email)
  if not db_user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email does not exist")
  verified = utils.verify_password(request.password, db_user.password)
  if not verified:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
  response = login_user(db_user)
  return response

def get_token_header(authorization: str = Header(...)):
    # You can add custom logic to validate or process the authorization header here
    return authorization

@router.get('/me')
def get_current_user(db:Session=Depends(db.get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
  token = credentials.credentials
  user = utils.get_current_user(token, db)
  del user.password
  return user

@router.post('/forgot-password/reset-link')
async def get_link_to_reset_password(request: schemas.ForgotPassword, db:Session=Depends(db.get_db)):
  db_user = get_user_by_email(db, email=request.email)
  if not db_user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Account with email does not exist")
  response = handle_forgot_pwd_req(db, db_user)
  return response

@router.post('/forgot-password/validate')
async def verify_forgot_password_request(request: schemas.ValidateForgotPasswordCode):
  utils.verify_token_access(request.token)
  return HTTPException(status_code=status.HTTP_200_OK, detail={"verified": True})

@router.post('/forgot-password/update')
async def set_new_password(request: schemas.ResetPassword, db:Session=Depends(db.get_db)):
  update_response = reset_user_password(request, db)
  return update_response
