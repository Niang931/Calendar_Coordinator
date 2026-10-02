import uuid
from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from app.core.utils import get_current_user, get_session
from app.schemas.user_schema import GroupCreate
from app.internal.group import add_user_to_group, add_group, get_group_id, is_already_in_group
from app.internal.user import get_user_id

router = APIRouter(prefix='/groups',
                   tags=['groups'])

@router.post('/create')
def create_group(group: GroupCreate, 
                 user_id: uuid.UUID = Depends(get_current_user),
                 session=Depends(get_session)):
    add_group(session=session, group=group)
    return 'succeed'
    
@router.post('/add-user')
def add_user(username: str, group_name: str,created_at: date = None,
                      session=Depends(get_session),
                      user_id=Depends(get_current_user)):
    add_user_id = get_user_id(username=username, session=session)
    group_id = get_group_id(group_name=group_name, created_at=created_at, session=session)
    add_user_to_group(user_id=add_user_id,
                      group_id=group_id,
                      session=session)
    return 
    
@router.post('/join-group')
def join_group(group_name: str,
               created_at: date = None,
               user_id=Depends(get_current_user),
               session=Depends(get_session)):
    group_id = get_group_id(group_name=group_name,
                            created_at=created_at,
                            session=session)
    if not group_id:
        raise HTTPException(status_code=404,
                            detail='Group not found')
    if is_already_in_group(user_id=user_id, group_id=group_id, session=session):
        raise HTTPException(status_code=403,
                            detail='User already in group')
    
    add_user_to_group(user_id=user_id,
                      group_id=group_id,
                      session=session)
    return 