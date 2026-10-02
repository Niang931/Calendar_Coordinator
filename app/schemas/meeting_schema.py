from pydantic import BaseModel
from datetime import date, time
from enum import Enum
from typing import Optional

class Level(Enum):
    low = 1
    medium = 2
    high = 3


class TimeSlotCheck(BaseModel):
    '''Request to meeting'''
    group_name: str
    meeting_date: date
    meeting_duration: float = 1.00
    
class TimeSlotProposal(TimeSlotCheck):
    title: str
    meeting_time: time
    reason: Optional[str]
    
    