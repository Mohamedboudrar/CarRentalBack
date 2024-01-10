from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app import models
from app.utils.jwt_utils import create_access_token, verify_token_access
from app.utils.password_utils import hash_password
from app.utils.mail_utils import send_mail
from app.schemas import auth_schemas
import uuid

def create_user(db: Session, body: auth_schemas.Register):
    hashed_pwd = hash_password(body.password)
    new_user = models.User(email=body.email, password=hashed_pwd, first_name=body.first_name, last_name=body.last_name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_user(user: models.User):
    access_token = create_access_token(
      data={"user_id": user.id}
    )
    return {"access_token": access_token, "token_type": "bearer"}

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def handle_forgot_pwd_req(db: Session, db_user: models.User):
    original_random_guid = str(uuid.uuid4())
    token= create_access_token(data={"token": original_random_guid, "user_id": db_user.id}, minutes=20)
    new_pwd_req = models.ForgotPasswordRequest(token=token)
    db.add(new_pwd_req)
    db.commit()
    db.refresh(new_pwd_req)
    # send mail
    url = "http://localhost/reset-password?token=" + token 
    html_content = "<html><body>Hello, click <a href=" + url + ">here</a> to proceed with password reset</body></html>"
    send_mail(to_email=db_user.email,
              subject="Password reset link",
              text_content=html_content)
    return {"message": "Reset link sent to your email address"}


def reset_user_password(body: auth_schemas.ResetPassword, db: Session):
    if body.password != body.confirm_password:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Passwords dont match")
    if not body.token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token not provided")
    is_verified_token = verify_token_access(body.token)
    # update user's password
    hashed_pwd = hash_password(body.password)
    db_user = db.get(models.User, is_verified_token.id)
    updated_user = models.User(id=is_verified_token.id, password=hashed_pwd)
    setattr(db_user, "password", updated_user.password)
    db.add(db_user)
    # delete token from table
    db.query(models.ForgotPasswordRequest).filter_by(token=body.token).delete()
    db.commit()
    db.refresh(db_user)
    return HTTPException(status_code=status.HTTP_200_OK, detail="Password successfully changed")