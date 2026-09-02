from sqlalchemy.orm import Session
from sqlalchemy import select
import uuid
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserDB

def get_user_by_username(username: str, session: Session):
    user = session.scalars(select(User).where(User.username==username)).first()
    return user

def get_user_by_id(user_id: uuid.UUID, session: Session):
    user = session.scalars(select(User).where(User.user_id==user_id)).one()
    return user
    
def add_user(user: UserDB, session: Session):
    '''Insert user into the table'''
    user = User(username=user.username,
                hashed_password=user.hashed_password,
                email=user.email)
    session.add(user)
    