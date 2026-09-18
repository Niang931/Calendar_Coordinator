import uuid
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy import exc
from datetime import date, time
from app.core.logger import logger
from app.core.database import get_session
from app.schemas.task_schema import Task, TaskDB
from app.internal.task import filter_task, add_task, modify_task, delete_task
from app.core.utils import get_current_user


router = APIRouter(prefix='/tasks',
                   tags=['tasks'])

@router.get('/{user_id}')
async def get_tasks(user_id: uuid.UUID=Depends(get_current_user),
                    session=Depends(get_session),
                    title: str = None, 
                    start_date: date= None):
    '''Show all the tasks set up by the user (based on user id)'''
    try:
        tasks:list[TaskDB] = filter_task(user_id, session, title=title, start_date=start_date)
        new_tasks = [Task(title=task.title, 
                    start_date=task.start_date,
                    start_time=task.start_time, 
                    duration=task.duration)
                for task in tasks]
        return new_tasks
    except exc.DatabaseError as e:
        logger.error(e)
        raise


@router.post('/{user_id}/create')
async def create_task(task: Task,
                      user_id: uuid.UUID=Depends(get_current_user),
                      session=Depends(get_session)):
    '''Add new task by the user id'''
    try:
        add_task(task, user_id, session)
        return 
    except exc.DataError as e:
        logger.error(e)
        raise
        
@router.put('/{user_id}/update')
async def update_task(title: str,
                      new_title: str,
                      new_start_date: date = None,
                      new_start_time: time = None,
                      start_date: date  = None,
                      user_id: uuid.UUID=Depends(get_current_user),
                      session=Depends(get_session)):
    task_to_update = filter_task(user_id=user_id,
                                 session=session,
                                 title=title,
                                 start_date=start_date)
    if not task_to_update:
        raise HTTPException(status_code=404,
                            detail='NO task found')
    modify_task(task_to_update=task_to_update,
                session=session,
                new_title=new_title,
                new_deadline=new_start_time,
                new_start_time=new_start_time)
    return 
    

@router.delete('/{uesr_id}/delete')
async def delete_task(title: str,
                      start_date: date = None,
                      user_id: uuid.UUID=Depends(get_current_user),
                      session=Depends(get_session)):
    task_to_delete = filter_task(user_id=user_id,
                                 session=session,
                                 title=title,
                                 start_date=start_date)
    if not task_to_delete:
        raise HTTPException(status_code=404,
                            detail='Task not found')
    delete_task(task_to_delete)
    return
