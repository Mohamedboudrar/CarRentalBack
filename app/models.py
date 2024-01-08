from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Date, UUID, Enum as sqlAlchemyEnum
import datetime as dt
from app.schemas import vehicle_schemas
from .db import Base
import uuid
from pydantic import Field

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4().hex, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    created_at = Column(DateTime, default=dt.datetime.now)
    

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4().hex, primary_key=True, index=True)
    user_id = Column(UUID, unique=True)
    first_name = Column(Text)
    last_name = Column(Text)
    
class ForgotPasswordRequest(Base):
    __tablename__ = "forgot_password_requests"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4().hex, primary_key=True, index=True)
    token = Column(Text)
    created_at = Column(DateTime, default=dt.datetime.now)
    

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4().hex, primary_key=True, index=True)
    name = Column(Text)
    model = Column(Text)
    description = Column(Text)
    user_id = Column(UUID)
    status = Column(sqlAlchemyEnum(vehicle_schemas.StatusEnum))
    created_at = Column(DateTime, default=dt.datetime.now)
    
class Booking(Base):
    __tablename__ = "bookings"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4().hex, primary_key=True, index=True)
    start_date = Column(Date)
    end_date = Column(Date)
    vehicle_id = Column(UUID)
    user_id = Column(UUID)
    is_confirmed = Column(Boolean, default=False)
    is_canceled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=dt.datetime.now)
    