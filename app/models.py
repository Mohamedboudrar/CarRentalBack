from sqlalchemy import Column, Integer, String, DateTime, Text
import datetime as dt

from .db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    created_at = Column(DateTime, default=dt.datetime.now)
    

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True)
    first_name = Column(Text)
    last_name = Column(Text)
    
class ForgotPasswordRequest(Base):
    __tablename__ = "forgot_password_requests"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(Text)
    created_at = Column(DateTime, default=dt.datetime.now)