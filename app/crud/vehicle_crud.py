from sqlalchemy.orm import Session
from app import models, db
from app.schemas import user_schemas, vehicle_schemas
from fastapi import Depends, HTTPException, status

def add_vehicle(db: Session, body: user_schemas.Profile, user_id: int):
    new_vehicle = models.Vehicle(user_id=user_id, name=body.name, model=body.model, description=body.description, status=body.status)
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)
    return {"message": "Vehicle created"}

def list_all_vehicles(db: Session, status: str):
    vehicles = db.query(models.Vehicle).filter(models.Vehicle.status == status).all()
    return vehicles
  
def get_vehicle_details(db: Session, vehicle_id: int):
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()
    return vehicle
  
def delete_vehicle(db: Session, vehicle_id: int):
    db.query(models.Vehicle).filter_by(id=vehicle_id).delete()
    db.commit()
    return HTTPException(status_code=status.HTTP_200_OK, detail="Vehicle deleted")
  
def handle_update_vehicle(db: Session, body: vehicle_schemas.AddVehicle, vehicle_id: int):
    db_user = db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id)
    db_user.update({"name": body.name, "model": body.model, "description": body.description, "status": body.status})
    db.commit()
    return {"message": "Vehicle has been updated"}