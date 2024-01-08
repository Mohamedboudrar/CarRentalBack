from fastapi import APIRouter, Security
from app.crud import booking_crud, user_crud
from app.schemas import booking_schemas
from fastapi import APIRouter, Depends, Security, HTTPException, status, Response
from sqlalchemy.orm import Session
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app import models, db
from app.utils import jwt_utils

security = HTTPBearer()

router = APIRouter()

@router.post('')
async def make_booking(request:booking_schemas.MakeBooking, db:Session=Depends(db.get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    user = jwt_utils.verify_token_access(token)
    response = booking_crud.handle_make_booking(request, db, user.id)
    return response

@router.put('/{booking_id}')
async def update_booking_detail():
    return {"message": "Booking updated"}

@router.get('/{booking_id}')
async def get_booking_detail():
    return {}


@router.put('/{booking_id}/confirm')
async def confirm_booking(booking_id: int, db:Session=Depends(db.get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    current_user = jwt_utils.verify_token_access(token)
    booking_detail = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    vehicle_detail = db.query(models.Vehicle).filter(models.Vehicle.id == booking_detail.vehicle_id).first()
    if str(vehicle_detail.user_id != current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You dont have the permission to confirm this booking")
    response = booking_crud.handle_booking_confirmation(db, booking_id)
    return response


@router.put('/{booking_id}/cancel')
async def cancel_booking(booking_id: int, db:Session=Depends(db.get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    current_user = jwt_utils.verify_token_access(token)
    booking_detail = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    vehicle_detail = db.query(models.Vehicle).filter(models.Vehicle.id == booking_detail.vehicle_id).first()

    if str(vehicle_detail.user_id) != str(current_user.id) or str(current_user.id) != str(booking_detail.user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You dont have the permission to cancel this booking")
    response = booking_crud.handle_booking_cancellation(db, booking_id)
    return response