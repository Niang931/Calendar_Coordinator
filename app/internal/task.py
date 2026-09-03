import uuid
from datetime import date, datetime
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.task_model import Task

def filter_task(user_id: uuid, 
                session: Session,
                title: str = None,
                deadline: datetime| date = None)-> list[Task]:
    statement = select(Task).where(Task.user_id==user_id)
    if title:
        statement = statement.where(Task.title==title)
    if deadline:
        statement = statement.where(Task.deadline==deadline)
    tasks = session.scalars(statement).all()
    return tasks

def add_task(task: Task, user_id: uuid.UUID, session: Session) -> None:
    '''Insert task based on the table with the user id'''
    taskdb = Task(title=task.title,
                    deadline=task.deadline,
                    duration=task.duration,
                    user_id=user_id)
    session.add(taskdb)
    
def modify_task(task_to_update: Task, 
                session: Session,
                new_title: str = None,
                new_deadline: datetime | date = None) -> None:
    if new_title:
        task_to_update.title = new_title
    if new_deadline:
        task_to_update.deadline = new_deadline
    session.commit()
    
def delete_task(task: Task,
                session: Session) -> None:
    session.delete(task)
    
        
