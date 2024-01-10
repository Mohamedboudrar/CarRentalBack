from fastapi import APIRouter, Request, Depends, HTTPException, status
from app.crud import booking_crud
from app.schemas import booking_schemas
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from app import models, db
from app.middleware import auth_dependency_middleware

security = HTTPBearer()

router = APIRouter()

@router.post('', dependencies=[Depends(auth_dependency_middleware())])
async def make_booking(request: Request, body:booking_schemas.MakeBooking, db:Session=Depends(db.get_db)):
    current_user_id = request.state.user.id
    response = booking_crud.handle_make_booking(body, db, current_user_id)
    return response


@router.put('/{booking_id}')
async def update_booking_detail():
    return {"message": "Booking updated"}


@router.get('/{booking_id}')
async def get_booking_detail():
    return {}


@router.put('/{booking_id}/confirm', dependencies=[Depends(auth_dependency_middleware())])
async def confirm_booking(request: Request, booking_id: str, db:Session=Depends(db.get_db)):
    current_user_id = request.state.user.id
    booking_detail = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    vehicle_detail = db.query(models.Vehicle).filter(models.Vehicle.id == booking_detail.vehicle_id).first()
    if str(vehicle_detail.user_id) != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You dont have the permission to confirm this booking")
    response = booking_crud.handle_booking_confirmation(db, booking_id)
    return response


@router.put('/{booking_id}/cancel', dependencies=[Depends(auth_dependency_middleware())])
async def cancel_booking(request: Request, booking_id: str, db:Session=Depends(db.get_db)):
    current_user_id = request.state.user.id
    booking_detail = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    vehicle_detail = db.query(models.Vehicle).filter(models.Vehicle.id == booking_detail.vehicle_id).first()

    if str(vehicle_detail.user_id) != current_user_id or current_user_id != str(booking_detail.user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You dont have the permission to cancel this booking")
    response = booking_crud.handle_booking_cancellation(db, booking_id)
    return response