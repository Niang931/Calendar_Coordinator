import uuid
from datetime import date, time
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.task_model import Task

def filter_task(user_id: uuid.UUID, 
                session: Session,
                title: str = None,
                start_date: date = None)-> list[Task]:
    statement = select(Task).where(Task.user_id==user_id)
    if title:
        statement = statement.where(Task.title==title)
    if start_date:
        statement = statement.where(Task.start_date==start_date)
    tasks = session.scalars(statement).all()
    return tasks

def add_task(task: Task, 
             user_id: uuid.UUID, 
             session: Session) -> None:
    '''Insert task based on the table with the user id'''
    taskdb = Task(title=task.title,
                    start_date=task.start_date,
                    start_time=task.start_time,
                    duration=task.duration,
                    user_id=user_id)
    session.add(taskdb)
    
def modify_task(task_to_update: Task, 
                session: Session,
                new_title: str = None,
                new_deadline: date = None,
                new_start_time: time = None) -> None:
    if new_title:
        task_to_update.title = new_title
    if new_deadline:
        task_to_update.start_date = new_deadline
    if new_start_time:
        task_to_update.start_time = new_start_time
    session.commit()
    
def delete_task(task: Task,
                session: Session) -> None:
    session.delete(task)
    
        
