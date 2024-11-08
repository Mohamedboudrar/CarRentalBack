from sqlalchemy.orm import Session
from fastapi import UploadFile
from app import models, db
from typing import Optional
from app.schemas import user_schemas, vehicle_schemas
import shutil
import uuid
import os

UPLOAD_DIRECTORY = "./static/images"  # Define the directory to store images (inside your project folder)

# Ensure the upload directory exists
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

def save_picture(picture: UploadFile) -> str:
    if picture:
        # Generate a unique filename and define save path
        file_extension = picture.filename.split(".")[-1]
        picture_filename = f"{uuid.uuid4()}.{file_extension}"
        picture_path = os.path.join(UPLOAD_DIRECTORY, picture_filename)

        # Save the uploaded file to specified path
        with open(picture_path, "wb") as f:
            shutil.copyfileobj(picture.file, f)  # Writes file content

        return f"/static/images/{picture_filename}"  # Path to be saved in database
    return None

async def add_vehicle(db: Session, body: user_schemas.Profile, user_id: str, picture: Optional[UploadFile] = None):
    # If a picture is provided, save it and get the file URL
    picture_url = await save_picture(picture) if picture else None

    # Create a new vehicle instance with all required fields
    new_vehicle = models.Vehicle(
        user_id=user_id,
        name=body.name,
        model=body.model,
        description=body.description,
        status=body.status,
        price=body.price,
        picture=picture_url  # Save the URL of the picture in the database
    )
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)
    return {"message": "Vehicle created"}

def list_all_vehicles(db: Session, status: str):
    """
    Get all vehicles with a specific status from the database.
    """
    vehicles = db.query(models.Vehicle).filter(models.Vehicle.status == status).all()
    return vehicles

def get_vehicle_details(db: Session, vehicle_id: str):
    """
    Get details of a specific vehicle by its ID.
    """
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()
    return vehicle

def delete_vehicle(db: Session, vehicle_id: str):
    """
    Delete a vehicle from the database by its ID.
    """
    db.query(models.Vehicle).filter_by(id=vehicle_id).delete()
    db.commit()
    return {"message": "Vehicle deleted"}

def handle_update_vehicle(db: Session, body: vehicle_schemas.AddVehicle, vehicle_id: str, picture: Optional[UploadFile] = None):
    """
    Update the details of a specific vehicle.
    If a new picture is provided, it will replace the old one.
    """
    # Query for the vehicle
    db_vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id)

    # If a new picture is provided, save it and get the file path
    picture_path = save_picture(picture) if picture else db_vehicle.first().picture

    # Update vehicle data
    db_vehicle.update({
        "name": body.name,
        "model": body.model,
        "description": body.description,
        "status": body.status,
        "price": body.price,
        "picture": picture_path
    })
    db.commit()
    return {"message": "Vehicle has been updated"}
