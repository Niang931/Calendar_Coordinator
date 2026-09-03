from pydantic import BaseModel
from datetime import datetime, date
import uuid

class Task(BaseModel):
    '''task with explicit timing and duration (class/ meeting)'''
    title: str
    deadline: datetime | date
    duration: float = 1.00

class TaskDB(Task):
    user_id: uuid.UUID
    task_id: uuid.UUID
    
