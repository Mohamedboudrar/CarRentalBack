from fastapi import APIRouter, Depends, Security, status, Response
from app import schemas, utils, db
from sqlalchemy.orm import Session
from app.crud.user import update_password

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer()

router = APIRouter()

@router.put('/')
async def update_profile():
  return {"message": "Profile updated"}

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

