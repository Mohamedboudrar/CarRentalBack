from fastapi import APIRouter, Depends, Security, HTTPException, status
from app.schemas import vehicle_schemas
from sqlalchemy.orm import Session
from app import models, db
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.crud import vehicle_crud, user_crud

security = HTTPBearer()

router = APIRouter()

@router.post('')
async def add_vehicle(request: vehicle_schemas.AddVehicle, db:Session=Depends(db.get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    user = user_crud.handle_get_current_user(token, db)
    response = vehicle_crud.add_vehicle(db, request, user.id)
    return response

@router.get('')
async def list_vehicles(status: str = 'available', db:Session=Depends(db.get_db)):
    vehicles = vehicle_crud.list_all_vehicles(db, status)
    return vehicles

@router.get('/{vehicle_id}')
async def vehicle_detail(id: str, db:Session=Depends(db.get_db)):
    response = vehicle_crud.get_vehicle_details(db, id)
    return response

@router.put('/{vehicle_id}')
async def update_vehicle(vehicle_id: str, request: vehicle_schemas.AddVehicle, db:Session=Depends(db.get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    user = user_crud.handle_get_current_user(token, db)
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
    if vehicle.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to update this vehicle because you dont own it")
    response = vehicle_crud.handle_update_vehicle(db, request, vehicle_id)
    return response

@router.delete('/{vehicle_id}')
async def delete_vehicle(vehicle_id: str, db:Session=Depends(db.get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    user = user_crud.handle_get_current_user(token, db)
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()
    if not vehicle:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
    if vehicle.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to delete this vehicle because you dont own it")
    if vehicle.status == vehicle_schemas.StatusEnum.active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to delete a currently active vehicle")
    response = vehicle_crud.delete_vehicle(db, vehicle_id)
    return response

@router.get('/{vehicle_id}/bookings')
async def vehicle_reservations(vehicle_id: str, db:Session=Depends(db.get_db)):
    vehicle_bookings = db.query(models.Booking).filter(models.Booking.vehicle_id == vehicle_id & models.Booking.is_canceled == False).all()
    return vehicle_bookings
