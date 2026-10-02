from sqlalchemy.orm import Session
from sqlalchemy import select
import uuid
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserDB

def get_user_id(session: Session,
                user_email: str = None,
                username: str = None):
    if username:
        user_id = session.scalars(select(User.user_id).where(User.username==username)).first()
    if user_email:
        user_id = session.scalars(select(User.user_id).where(User.email==user_email)).first()
    return user_id

def get_user(session: Session, 
                         username: str= None, 
                         user_id: uuid.UUID = None):
    if username:
        user = session.scalars(select(User).where(User.username==username)).first()
    elif user_id:
        user = session.scalars(select(User).where(User.user_id==user_id)).one()
    return user

def add_user(user: UserDB, session: Session):
    '''Insert user into the table'''
    user = User(username=user.username,
                hashed_password=user.hashed_password,
                email=user.email)
    session.add(user)
    