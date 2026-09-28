import uuid
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime
from app.models.user_model import User
from app.models.group_model import Group, User_Group
from app.schemas.user_schema import GroupCreate

def add_group( session: Session,
                group: GroupCreate):
    groupdb = Group(group_name=group.group_name,
                    group_description=group.group_description)
    session.add(groupdb)

def get_group_id(group_name: str,
                 session: Session,
                 created_at: Optional[datetime]=None):
    if group_name:
        stmt = select(Group.group_id).where(Group.group_name==group_name)
    if created_at:
        stmt = stmt.where(Group.created_at==created_at)
    group_id = session.scalars(stmt).one_or_none()
    return group_id
    
def add_user_to_group(user_id: uuid.UUID,
                      group_id: uuid.UUID,
                      session: Session):
    user_group = User_Group(user_id = user_id,
                            group_id=group_id)
    session.add(user_group)
    
def get_user_in_group(group_id: uuid.UUID,
                      session: Session):
    user_ids = session.scalars(select(User_Group.user_id).where(User_Group.group_id==group_id)).all()
    # usernames = []
    # for user_id in user_ids:
    #     username = session.scalars(select(User.username).where(User.user_id==user_id)).first()
    #     usernames.append(username)
    return user_ids

def is_already_in_group(user_id: uuid.UUID,
                        group_id: uuid.UUID,
                        session: Session):
    find_user_id = session.scalars(select(User_Group.user_id).where(User_Group.group_id==group_id)).all()
    return user_id in find_user_id

