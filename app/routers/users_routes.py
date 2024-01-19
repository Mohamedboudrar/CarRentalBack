from fastapi import APIRouter, Depends, status, Response, Request
from app import db
from sqlalchemy.orm import Session
from app import models
from app.schemas import user_schemas
from app.utils.password_utils import verify_password
from app.crud import user_crud
from app.middleware import auth_dependency_middleware
from fastapi.security import HTTPBearer

security = HTTPBearer()

router = APIRouter()


@router.post('/change-password', dependencies=[Depends(auth_dependency_middleware())])
async def reset_password(body: user_schemas.ChangePassword, response: Response, request: Request, db:Session=Depends(db.get_db)):
    user = user_crud.get_user_profile(response, request.state.user.id, db)
    is_verified_password = verify_password(body.current_password, user.password)
    if (is_verified_password):
        response = user_crud.update_password(db, body.new_password, user.id)
        return response
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "Current password is incorrect"}


@router.get('/me/vehicles', dependencies=[Depends(auth_dependency_middleware())])
async def fetch_current_user_vehicles(request: Request, db:Session=Depends(db.get_db)):
    current_user_id = request.state.user.id
    profile = db.query(models.Vehicle).filter(models.Vehicle.user_id == current_user_id).all()
    return profile


@router.get('/profile/{user_id}')
async def fetch_user_profile(response: Response, id: str, db:Session=Depends(db.get_db)):
    crud_response = user_crud.get_user_profile(response, id, db)
    return crud_response


@router.put('/profile', dependencies=[Depends(auth_dependency_middleware())])
async def update_current_user_profile(response: Response, request: Request, body: user_schemas.Profile, db:Session=Depends(db.get_db)):
    current_user_id = request.state.user.id
    update_response = user_crud.handle_update_current_user_profile(db, body, current_user_id)
    response.status_code = status.HTTP_200_OK
    return update_response