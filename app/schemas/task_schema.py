from pydantic import BaseModel
from datetime import date, time
import uuid

class Task(BaseModel):
    '''task with explicit timing and duration (class/ meeting)'''
    title: str
    start_date: date
    start_time: time
    duration: float = 1.00
    participants : list[str] =[]

class TaskDB(Task):
    user_id: uuid.UUID
    task_id: uuid.UUID
    
