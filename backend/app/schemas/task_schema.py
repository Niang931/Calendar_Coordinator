from pydantic import BaseModel
from datetime import datetime

class Goal(BaseModel):
    
    user_id: str
    task_id: str
    datetime: datetime

class Task(Goal):

    duration: float = 1.00


