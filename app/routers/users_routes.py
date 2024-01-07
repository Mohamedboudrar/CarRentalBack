from fastapi import APIRouter, Depends, Security, status, Response
from app import db
from sqlalchemy.orm import Session
from app import models
from app.schemas import user_schemas
from app.utils.jwt_utils import verify_token_access
from app.utils.password_utils import verify_password
from app.crud import user_crud

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer()

router = APIRouter()

@router.post('/change-password')
async def reset_password(request: user_schemas.ChangePassword, response: Response, db:Session=Depends(db.get_db),  credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    user = user_crud.handle_get_current_user(token, db)
    is_verified_password = verify_password(request.current_password, user.password)
    if (is_verified_password):
        response = user_crud.update_password(db, request.new_password, user.id)
        return response
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "Current password is incorrect"}


@router.post('/profile')
async def create_current_user_profile(response: Response, request: user_schemas.Profile, db:Session=Depends(db.get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    current_user = verify_token_access(token)
    profile_exists = db.query(models.Profile).filter(models.Profile.user_id == current_user.id).first()
    if profile_exists:
        response.status_code = status.HTTP_409_CONFLICT
        return {"message": "profile already exists"}
    response = user_crud.create_user_profile(db, request, current_user.id)
    return response

@router.get('/me/profile')
async def fetch_current_user_profile(db:Session=Depends(db.get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    current_user = verify_token_access(token)
    profile = db.query(models.Profile).filter(models.Profile.user_id == current_user.id).first()
    return profile

@router.get('/me/vehicles')
async def fetch_current_user_vehicles(db:Session=Depends(db.get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    current_user = verify_token_access(token)
    profile = db.query(models.Vehicle).filter(models.Vehicle.user_id == current_user.id).all()
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
async def update_current_user_profile(response: Response, request: user_schemas.Profile, db:Session=Depends(db.get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    current_user = verify_token_access(token)
    update_response = user_crud.handle_update_current_user_profile(db, request, current_user.id)
    response.status_code = status.HTTP_200_OK
    return update_response