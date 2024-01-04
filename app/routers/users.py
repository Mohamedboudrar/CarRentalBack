from fastapi import APIRouter, Depends, Security, status, Response
from app import schemas, utils, db
from sqlalchemy.orm import Session
from app.crud.user import update_password, create_user_profile, handle_update_current_user_profile
from app import models, utils

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer()

router = APIRouter()


@router.post('/change-password')
async def reset_password(request: schemas.ChangePassword, response: Response, db:Session=Depends(db.get_db),  credentials: HTTPAuthorizationCredentials = Security(security)):
  token = credentials.credentials
  user = utils.get_current_user(token, db)
  is_verified_password = utils.verify_password(request.current_password, user.password)
  if (is_verified_password):
    response = update_password(db, request.new_password, user.id)
    return response
  else:
    response.status_code = status.HTTP_401_UNAUTHORIZED
    return {"message": "Current password is incorrect"}


@router.post('/profile')
async def create_current_user_profile(response: Response, request: schemas.Profile, db:Session=Depends(db.get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
  token = credentials.credentials
  utils.verify_token_access(token)
  user = utils.get_current_user(token, db)
  profile_exists = db.query(models.Profile).filter(models.Profile.user_id == user.id).first()
  if profile_exists:
    response.status_code = status.HTTP_409_CONFLICT
    return {"message": "profile already exists"}
  response = create_user_profile(db, request, user.id)
  return response

@router.get('/profile/me')
async def fetch_current_user_profile(db:Session=Depends(db.get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
  token = credentials.credentials
  utils.verify_token_access(token)
  user = utils.get_current_user(token, db)
  profile = db.query(models.Profile).filter(models.Profile.user_id == user.id).first()
  return profile

@router.get('/profile/{user_id}')
async def fetch_user_profile(response: Response, id: str, db:Session=Depends(db.get_db)):
  profile_exists = db.query(models.Profile).filter(models.Profile.user_id == id).first()
  if not profile_exists:
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"message": "profile NOT FOUND"}
  response.status_code = status.HTTP_200_OK
  return profile_exists

@router.put('/profile')
async def update_current_user_profile(response: Response, request: schemas.Profile, db:Session=Depends(db.get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
  token = credentials.credentials
  utils.verify_token_access(token)
  user = utils.get_current_user(token, db)
  update_response = handle_update_current_user_profile(db, request, user.id)
  response.status_code = status.HTTP_200_OK
  return update_response