from sqlalchemy.orm import Session
from app import models, db
from fastapi import HTTPException, status, Response
from app.schemas import booking_schemas
from app.utils.mail_utils import send_mail

def send_booking_confirmation_mail(vehicle_owner_email, booker_detail_email):
    send_mail(to_email=vehicle_owner_email,
              subject="Booking alert",
              text_content="<html><body>Hello, a vehicle has just been booked. Click <a href='http://localhost/dashboard'>here</a> to see details in the dashboard</body></html>")
    send_mail(to_email=booker_detail_email,
              subject="Vehicle booked",
              text_content="<html><body>Hello, vehicle has been booked. await confirmation from host</body></html>")
  
def handle_make_booking(body: booking_schemas.MakeBooking, db: Session, user_id: int):
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == body.vehicle_id).first()
    conflicting_vehicle_bookings = db.query(models.Booking)\
                                  .filter(models.Booking.vehicle_id == body.vehicle_id)\
                                  .filter((body.start_date <= models.Booking.end_date) & (body.end_date >= models.Booking.start_date))\
                                  .filter(models.Booking.is_canceled == False)\
                                  .all()
    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle does not exist")
    if vehicle.user_id == user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot book a vehicle you own")
    if body.start_date > body.end_date:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Start date cannot come after end date")
    if conflicting_vehicle_bookings:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Vehicle has already been reserved at this time. Select a different date range")
    new_booking = models.Booking(vehicle_id=body.vehicle_id, start_date=body.start_date, end_date=body.end_date, user_id=user_id)
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    print(new_booking.end_date)
    # send booking mail to owner of vehicle and user
    vehicle_owner_detail = db.query(models.User).filter(models.User.id == vehicle.user_id).first()
    booker_detail = db.query(models.User).filter(models.User.id == user_id).first()
    send_booking_confirmation_mail(vehicle_owner_detail.email, booker_detail.email)
    return {"message": "Booking successful"}
  
def handle_booking_confirmation(db: Session, booking_id: int):
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id)
    booking.update({"is_confirmed": True})
    db.commit()
    return {"message": "Booking confirmed"}
  
  
def handle_booking_cancellation(db: Session, booking_id: int):
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id)
    booking.update({"is_canceled": True})
    db.commit()
    return {"message": "Booking canceled"}