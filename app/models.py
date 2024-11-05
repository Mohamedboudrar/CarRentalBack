from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Date, Enum as sqlAlchemyEnum
import datetime as dt
from app.schemas import vehicle_schemas
from .db import Base
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), default=lambda: str(uuid.uuid4()), primary_key=True, index=True)  # Use CHAR(36) for UUID
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))  # Add length for consistency
    first_name = Column(Text)
    last_name = Column(Text)
    created_at = Column(DateTime, default=dt.datetime.now)

class ForgotPasswordRequest(Base):
    __tablename__ = "forgot_password_requests"

    id = Column(String(36), default=lambda: str(uuid.uuid4()), primary_key=True, index=True)
    token = Column(Text)
    created_at = Column(DateTime, default=dt.datetime.now)

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(String(36), default=lambda: str(uuid.uuid4()), primary_key=True, index=True)
    name = Column(Text)
    model = Column(Text)
    description = Column(Text)
    user_id = Column(String(36))
    status = Column(sqlAlchemyEnum(vehicle_schemas.StatusEnum))
    created_at = Column(DateTime, default=dt.datetime.now)

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(String(36), default=lambda: str(uuid.uuid4()), primary_key=True, index=True)
    start_date = Column(Date)
    end_date = Column(Date)
    vehicle_id = Column(String(36))
    user_id = Column(String(36))
    is_confirmed = Column(Boolean, default=False)
    is_canceled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=dt.datetime.now)
