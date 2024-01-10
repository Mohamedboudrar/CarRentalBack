from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.schemas import vehicle_schemas
from sqlalchemy.orm import Session
from app import models, db
from fastapi.security import HTTPBearer
from app.crud import vehicle_crud
from app.middleware import auth_dependency_middleware

security = HTTPBearer()

router = APIRouter()


@router.post('', dependencies=[Depends(auth_dependency_middleware())])
async def add_vehicle(request: Request, body: vehicle_schemas.AddVehicle, db:Session=Depends(db.get_db)):
    current_user_id = request.state.user.id
    response = vehicle_crud.add_vehicle(db, body, current_user_id)
    return response


@router.get('')
async def list_vehicles(status: str = 'available', db:Session=Depends(db.get_db)):
    vehicles = vehicle_crud.list_all_vehicles(db, status)
    return vehicles


@router.get('/{vehicle_id}')
async def vehicle_detail(id: str, db:Session=Depends(db.get_db)):
    response = vehicle_crud.get_vehicle_details(db, id)
    return response


@router.put('/{vehicle_id}', dependencies=[Depends(auth_dependency_middleware())])
async def update_vehicle(request: Request, vehicle_id: str, body: vehicle_schemas.AddVehicle, db:Session=Depends(db.get_db)):
    current_user_id = request.state.user.id
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
    if str(vehicle.user_id) != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to update this vehicle because you dont own it")
    response = vehicle_crud.handle_update_vehicle(db, body, vehicle_id)
    return response


@router.delete('/{vehicle_id}', dependencies=[Depends(auth_dependency_middleware())])
async def delete_vehicle(request: Request, vehicle_id: str, db:Session=Depends(db.get_db)):
    current_user_id = request.state.user.id
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()
    if not vehicle:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
    if str(vehicle.user_id) != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to delete this vehicle because you dont own it")
    if vehicle.status == vehicle_schemas.StatusEnum.active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to delete a currently active vehicle")
    response = vehicle_crud.delete_vehicle(db, vehicle_id)
    return response


@router.get('/{vehicle_id}/bookings')
async def vehicle_reservations(vehicle_id: str, db:Session=Depends(db.get_db)):
    vehicle_bookings = db.query(models.Booking).filter(models.Booking.vehicle_id == vehicle_id & models.Booking.is_canceled == False).all()
    return vehicle_bookings
