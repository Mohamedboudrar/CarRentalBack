from fastapi import APIRouter, Depends, Response, HTTPException, Header, Security, status
from app import models, db
from app.utils.password_utils import verify_password
from app.utils.jwt_utils import verify_token_access
from sqlalchemy.orm import Session
from app.crud import auth_crud, user_crud

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.schemas import auth_schemas

security = HTTPBearer()

models.Base.metadata.create_all(bind=db.engine)

router = APIRouter()

@router.post('/register')
async def register(request: auth_schemas.RequestUser, db:Session=Depends(db.get_db)):
  db_user = auth_crud.get_user_by_email(db, email=request.email)
  if db_user:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
  auth_crud.create_user(db, request)
  return Response(
    status_code=201
  )
  
@router.post('/login')
async def login(request: auth_schemas.RequestUser, db:Session=Depends(db.get_db)):
  db_user = auth_crud.get_user_by_email(db, email=request.email)
  if not db_user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email does not exist")
  verified = verify_password(request.password, db_user.password)
  if not verified:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
  response = auth_crud.login_user(db_user)
  return response

def get_token_header(authorization: str = Header(...)):
    # You can add custom logic to validate or process the authorization header here
    return authorization

@router.get('/me')
def get_current_user(db:Session=Depends(db.get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
  token = credentials.credentials
  user = user_crud.handle_get_current_user(token, db)
  del user.password
  return user

@router.post('/forgot-password/reset-link')
async def get_link_to_reset_password(request: auth_schemas.ForgotPassword, db:Session=Depends(db.get_db)):
  db_user = auth_crud.get_user_by_email(db, email=request.email)
  if not db_user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Account with email does not exist")
  response = auth_crud.handle_forgot_pwd_req(db, db_user)
  return response

@router.post('/forgot-password/validate')
async def verify_forgot_password_request(request: auth_schemas.ValidateForgotPasswordCode):
  verify_token_access(request.token)
  return HTTPException(status_code=status.HTTP_200_OK, detail={"verified": True})

@router.post('/forgot-password/update')
async def set_new_password(request: auth_schemas.ResetPassword, db:Session=Depends(db.get_db)):
  update_response = auth_crud.reset_user_password(request, db)
  return update_response
