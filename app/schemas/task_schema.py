from pydantic import BaseModel
from datetime import datetime, date

class Base(BaseModel):
    
    user_id: str
    task_id: str

class Task(Base):
    '''task with explicit timing and duration (class/ meeting)'''
    datetime: datetime 
    duration: float = 1.00


class Goal(Base):
    '''The task without specific duration and time'''
    deadline: date
    